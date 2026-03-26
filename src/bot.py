import os
import json
import aiohttp
import discord
from discord import app_commands
from dotenv import load_dotenv
import asyncio
import logging
from datetime import datetime, timedelta

# Ρύθμιση Logging σε ΑΡΧΕΙΟ
log_file = "/home/harold/.openclaw/workspace/projects/orderly_docs/orderly_bot.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
)
logger = logging.getLogger("OrderlyBot")

# ── Opencode Serve Config ─────────────────────────────────────────────────────
OPENCODE_BIN  = "/home/harold/.opencode/bin/opencode"
OPENCODE_PORT = int(os.getenv("OPENCODE_PORT", 4096))
OPENCODE_URL  = f"http://127.0.0.1:{OPENCODE_PORT}"
SESSION_FILE  = os.path.join(os.path.dirname(__file__), "..", "opencode_session.json")
INACTIVITY_MINUTES = 10
DELETE_AFTER_MINUTES = 30

# Shared mutable state
_opencode_proc  = None   # the subprocess handle
_session_id     = None   # current opencode session ID
_last_activity  = datetime.utcnow()
_pending_deletes = []    # list of (discord.Message, datetime)


# ── Opencode Serve helpers ────────────────────────────────────────────────────

async def _start_opencode_serve():
    """Spawn opencode serve in background and wait until ready."""
    global _opencode_proc
    _opencode_proc = await asyncio.create_subprocess_exec(
        OPENCODE_BIN, "serve", "--port", str(OPENCODE_PORT),
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL,
    )
    logger.info(f"Spawned opencode serve PID={_opencode_proc.pid} on port {OPENCODE_PORT}")
    # Poll until server responds
    for _ in range(20):
        await asyncio.sleep(0.5)
        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(f"{OPENCODE_URL}/session", timeout=aiohttp.ClientTimeout(total=2)) as r:
                    if r.status < 500:
                        logger.info("Opencode serve is ready")
                        return
        except Exception:
            pass
    logger.warning("Opencode serve may not be ready yet; continuing anyway")


async def _load_or_create_session() -> str:
    """Load existing session ID from disk or create a new one."""
    global _session_id
    path = SESSION_FILE
    if os.path.exists(path):
        with open(path) as f:
            data = json.load(f)
            _session_id = data.get("session_id")
            if _session_id:
                logger.info(f"Loaded existing session: {_session_id}")
                return _session_id
    return await _create_new_session()


async def _create_new_session() -> str:
    """Create a fresh opencode session and persist its ID."""
    global _session_id
    async with aiohttp.ClientSession() as s:
        async with s.post(
            f"{OPENCODE_URL}/session",
            json={"title": "Discord Chat"},
            timeout=aiohttp.ClientTimeout(total=10),
        ) as r:
            data = await r.json()
            _session_id = data["id"]
    with open(SESSION_FILE, "w") as f:
        json.dump({"session_id": _session_id}, f)
    logger.info(f"Created new session: {_session_id}")
    return _session_id


async def _send_chat(user_name: str, text: str) -> str:
    """Send a message to the current opencode session and return the assistant reply."""
    global _last_activity
    _last_activity = datetime.utcnow()
    payload = {
        "parts": [{"type": "text", "text": f"{user_name}: {text}"}],
        "agent": "build",
    }
    async with aiohttp.ClientSession() as s:
        async with s.post(
            f"{OPENCODE_URL}/session/{_session_id}/message",
            json=payload,
            timeout=aiohttp.ClientTimeout(total=60),
        ) as r:
            if r.status != 200:
                return f"⚠️ Opencode error {r.status}"
            data = await r.json()
    # Response: list of messages, last one is the assistant reply
    try:
        messages = data if isinstance(data, list) else data.get("messages", [])
        # Find last message with role=assistant
        for msg in reversed(messages):
            if msg.get("role") == "assistant":
                parts = msg.get("parts", [])
                for part in reversed(parts):
                    if part.get("type") == "text" and part.get("text"):
                        return part["text"].strip()
        return str(data)
    except Exception as e:
        return f"⚠️ Parse error: {e}"


def process_idea_command(vm_instance, text, user_name):
    vm_instance.write_to_vault("meta/idea-dump", text, user_name)
    return "💡 Idea added!"


def process_question_command(vm_instance, text, user_name):
    vm_instance.write_to_vault("meta/open-questions", text, user_name)
    return "❓ Question added!"


def process_poll_command(vm_instance, text, user_name):
    vm_instance.write_to_vault("meta/polls", text, user_name)
    return f"📊 Poll added!"


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
VAULT_PATH = os.getenv("VAULT_PATH")

from vault_manager import VaultManager

vm = VaultManager(VAULT_PATH)

CHANNELS_MAP = {
    "architecture": "architecture/overview",
    "design": "design/overview",
    "ordering-flow": "architecture/ordering-flow",
    "ideas": "meta/idea-dump",
    "decisions": "meta/decisions",
    "polls": "meta/polls",
    "questions": "meta/open-questions",
}


class OrderlyBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.reactions = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.synced = False

    async def setup_hook(self):
        # Global sync can be slow, we'll use guild-level sync for instant updates in on_ready
        pass


bot = OrderlyBot()


@bot.event
async def on_ready():
    if bot.synced:
        return
    logger.info(f"SUCCESS: Logged in as {bot.user} (ID: {bot.user.id})")

    # Instant Sync for all guilds
    for guild in bot.guilds:
        try:
            bot.tree.copy_global_to(guild=guild)
            await bot.tree.sync(guild=guild)
            logger.info(f"Synced commands to Guild: {guild.name} ({guild.id})")
        except Exception as e:
            logger.error(f"Failed to sync to guild {guild.id}: {e}")

    # Spawn opencode serve and initialize session
    await _start_opencode_serve()
    await _load_or_create_session()

    bot.loop.create_task(update_all_channels())
    bot.loop.create_task(_check_inactivity())
    bot.loop.create_task(_delete_old_messages())
    bot.synced = True


async def _check_inactivity():
    """Every 30 s: reset session if chat has been idle for INACTIVITY_MINUTES."""
    while True:
        await asyncio.sleep(30)
        idle = datetime.utcnow() - _last_activity
        if idle > timedelta(minutes=INACTIVITY_MINUTES):
            logger.info(f"Inactivity ({int(idle.total_seconds()//60)} min) → creating new session")
            await _create_new_session()
            for guild in bot.guilds:
                ch = discord.utils.get(guild.text_channels, name="chat")
                if ch:
                    await ch.send("🔄 *Context cleared due to inactivity — new session started.*")


async def _delete_old_messages():
    """Every 10 s: delete bot messages that have passed DELETE_AFTER_MINUTES."""
    global _pending_deletes
    while True:
        await asyncio.sleep(10)
        now = datetime.utcnow()
        remaining = []
        for msg, delete_at in _pending_deletes:
            if now >= delete_at:
                try:
                    await msg.delete()
                    logger.info("Auto-deleted bot message")
                except Exception:
                    pass
            else:
                remaining.append((msg, delete_at))
        _pending_deletes = remaining



async def update_all_channels():
    logger.info("Starting background vault sync...")
    for guild in bot.guilds:
        for channel_name, vault_topic in CHANNELS_MAP.items():
            channel = discord.utils.get(guild.text_channels, name=channel_name)
            if channel:
                await silent_update_channel(channel, vault_topic, channel_name.title())
                await asyncio.sleep(2)
    logger.info("Background vault sync finished.")


async def silent_update_channel(channel, vault_topic, title):
    try:
        content = ""
        if vault_topic == "meta/polls":
            # Handle JSON polls
            file_path = os.path.join(VAULT_PATH, "meta/polls.json")
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    try:
                        polls_data = json.load(f)
                        if not polls_data:
                            content = "No active polls."
                        else:
                            for p_id, p_info in polls_data.items():
                                votes_count = len(p_info.get("votes", []))
                                content += f"- {p_info['text']} (by {p_info['author']}) - 📈 {votes_count}/4 votes\n"
                    except:
                        content = "Error reading polls JSON."
            else:
                content = "No active polls."
        else:
            # Handle standard markdown
            content = await asyncio.to_thread(vm.read_from_vault, vault_topic)

        github_link = (
            f"https://github.com/dolly450/orderly_docs/blob/master/{vault_topic}.md"
        )
        if vault_topic == "meta/polls":
            github_link = (
                f"https://github.com/dolly450/orderly_docs/blob/master/meta/polls.json"
            )

        if len(content) > 1800:
            content = content[:1800] + "... (truncated)"

        msg_text = (
            f"🚀 **Orderly Vault: {title}**\n"
            f"🔗 **Archive:** {github_link}\n\n"
            f"**Content:**\n```markdown\n{content}\n```\n"
            f"*Last Sync: {discord.utils.utcnow().strftime('%H:%M:%S UTC')}*"
        )

        pins = await channel.pins()
        existing_pin = next((p for p in pins if p.author == bot.user), None)

        if existing_pin:
            await existing_pin.edit(content=msg_text)
            logger.info(f"Updated pin in #{channel.name}")
        else:
            new_msg = await channel.send(msg_text)
            await new_msg.pin()
            logger.info(f"Created new pin in #{channel.name}")

    except Exception as e:
        logger.error(f"Error in #{channel.name}: {e}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.channel.name == "chat":
        global _last_activity
        _last_activity = datetime.utcnow()
        async with message.channel.typing():
            try:
                response = await _send_chat(message.author.global_name or message.author.name, message.content)
                bot_msg = await message.reply(response)
                # Schedule auto-delete
                _pending_deletes.append((bot_msg, datetime.utcnow() + timedelta(minutes=DELETE_AFTER_MINUTES)))
            except Exception as e:
                logger.error(f"Chat error: {e}")
                await message.reply(f"⚠️ Σφάλμα: {str(e)[:200]}")


@bot.tree.command(name="idea", description="Καταγραφή ιδέας")
async def idea(interaction: discord.Interaction, text: str):
    await interaction.response.defer()
    user_name = interaction.user.global_name or interaction.user.name
    try:
        result_msg = await asyncio.to_thread(process_idea_command, vm, text, user_name)
        await interaction.followup.send(result_msg)

        # Update ONLY the dedicated #ideas channel
        dedicated_channel = discord.utils.get(
            interaction.guild.text_channels, name="ideas"
        )
        if dedicated_channel:
            bot.loop.create_task(
                silent_update_channel(dedicated_channel, "meta/idea-dump", "Idea Dump")
            )
        else:
            logger.warning("Dedicated #ideas channel not found for pinning.")

    except Exception as e:
        logger.error(f"Idea command error: {e}")
        await interaction.followup.send("Failed to log idea due to an internal error.")


@bot.tree.command(name="question", description="Καταγραφή ερώτησης")
async def question(interaction: discord.Interaction, text: str):
    await interaction.response.defer()
    user_name = interaction.user.global_name or interaction.user.name
    try:
        result_msg = await asyncio.to_thread(
            process_question_command, vm, text, user_name
        )
        await interaction.followup.send(result_msg)

        # Update ONLY the dedicated #questions channel
        dedicated_channel = discord.utils.get(
            interaction.guild.text_channels, name="questions"
        )
        if dedicated_channel:
            bot.loop.create_task(
                silent_update_channel(
                    dedicated_channel, "meta/open-questions", "Questions"
                )
            )
        else:
            logger.warning("Dedicated #questions channel not found for pinning.")

    except Exception as e:
        logger.error(f"Question command error: {e}")
        await interaction.followup.send(
            "Failed to log question due to an internal error."
        )


@bot.tree.command(name="poll", description="Καταγραφή ψηφοφορίας")
async def poll(interaction: discord.Interaction, text: str):
    await interaction.response.defer()
    user_name = interaction.user.global_name or interaction.user.name
    try:
        # We'll use the interaction ID as a base for poll ID
        poll_id = f"poll-{interaction.id}"

        # Write to JSON vault
        await asyncio.to_thread(vm.write_poll, poll_id, text, user_name)

        poll_msg = await interaction.followup.send(
            f"📊 **Poll by {user_name}**: {text}\n"
            f"React with ✅ to approve. (ID: `{poll_id}`)"
        )

        # Update ONLY the dedicated #polls channel pin
        dedicated_channel = discord.utils.get(
            interaction.guild.text_channels, name="polls"
        )
        if dedicated_channel:
            bot.loop.create_task(
                silent_update_channel(dedicated_channel, "meta/polls", "Polls")
            )
        else:
            logger.warning("Dedicated #polls channel not found for pinning.")

        # Add initial reaction
        await poll_msg.add_reaction("✅")
    except Exception as e:
        logger.error(f"Poll command error: {e}")
        await interaction.followup.send("Failed to log poll due to an internal error.")


@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:
        return

    if payload.emoji.name == "✅":
        channel = bot.get_channel(payload.channel_id)
        if not channel:
            return

        try:
            msg = await channel.fetch_message(payload.message_id)
            if (
                msg.author == bot.user
                and "📊 **Poll by" in msg.content
                and "(ID: `poll-" in msg.content
            ):
                # Extract poll ID
                import re

                match = re.search(r"\(ID: `(poll-\d+)`\)", msg.content)
                if not match:
                    return
                poll_id = match.group(1)

                # Sync vote to JSON
                user_id = str(payload.user_id)
                await asyncio.to_thread(vm.add_vote, poll_id, user_id)

                # Check threshold (using reaction count is safer as it represents current state)
                for reaction in msg.reactions:
                    if str(reaction.emoji) == "✅" and reaction.count >= 4:
                        # Threshold reached! Archive it
                        await asyncio.to_thread(vm.archive_poll, poll_id)

                        # Delete the discord poll message
                        await msg.delete()

                        # Update pins for both polls and decisions
                        polls_channel = discord.utils.get(
                            channel.guild.text_channels, name="polls"
                        )
                        if polls_channel:
                            bot.loop.create_task(
                                silent_update_channel(
                                    polls_channel, "meta/polls", "Polls"
                                )
                            )

                        decisions_channel = discord.utils.get(
                            channel.guild.text_channels, name="decisions"
                        )
                        if decisions_channel:
                            bot.loop.create_task(
                                silent_update_channel(
                                    decisions_channel, "meta/decisions", "Decisions"
                                )
                            )
                        break
                else:
                    # Just update the polls pin to show new vote count
                    polls_channel = discord.utils.get(
                        channel.guild.text_channels, name="polls"
                    )
                    if polls_channel:
                        bot.loop.create_task(
                            silent_update_channel(polls_channel, "meta/polls", "Polls")
                        )

        except Exception as e:
            logger.error(f"Reaction handler error: {e}")


if __name__ == "__main__":
    if not TOKEN:
        logger.error("NO DISCORD_TOKEN FOUND IN .ENV!")
    else:
        bot.run(TOKEN)
