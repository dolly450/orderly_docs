import os
import re
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
OPENCODE_URL  = f"http://192.168.0.204:{OPENCODE_PORT}"
SESSION_FILE  = os.path.join(os.path.dirname(__file__), "..", "opencode_session.json")
INACTIVITY_MINUTES = 60


# Shared mutable state
_opencode_proc  = None   # the subprocess handle
_session_id     = None   # current opencode session ID
_last_activity  = datetime.utcnow()



# ── Opencode Serve helpers ────────────────────────────────────────────────────

async def _start_opencode_serve():
    """Spawn opencode serve in background and wait until ready."""
    global _opencode_proc
    _opencode_proc = await asyncio.create_subprocess_exec(
        OPENCODE_BIN, "serve", "--hostname", "0.0.0.0", "--port", str(OPENCODE_PORT),
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

    # Append Planka card-detection instruction if enabled
    planka_suffix = ""
    if _planka_enabled and _planka_client:
        labels_str = ", ".join(f'"{n}"' for n in _planka_client.get_label_names())
        planka_suffix = _build_planka_instruction(labels_str)

    payload = {
        "parts": [{"type": "text", "text": f"{user_name}: {text}{planka_suffix}"}],
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
    # Response: object with "parts" array
    try:
        parts = data.get("parts", [])
        # Extract only "text" parts (skip reasoning, step markers)
        text_parts = [p["text"] for p in parts if p.get("type") == "text" and p.get("text")]
        response = "\n".join(text_parts).strip()

        if not response:
            # Fallback to any text found in parts if no explicit "text" type
            response = "\n".join([str(p.get("text", "")) for p in parts if p.get("text")]).strip()

        # Process Planka card block if present
        if _planka_enabled and _planka_client:
            response, card_msg = await _process_planka_block(response)
            if card_msg:
                response = response + f"\n{card_msg}"

        # Truncate to avoid Discord 400 error (2k limit)
        if len(response) > 1900:
            response = response[:1900] + "... (truncated)"

        return response if response else "⚠️ Opencode returned an empty response."
    except Exception as e:
        logger.error(f"Parse error: {e} | Data: {str(data)[:200]}")
        return f"⚠️ Parse error: {str(e)[:100]}"


# ── Planka helpers ────────────────────────────────────────────────────────────

_PLANKA_BLOCK_RE = re.compile(
    r"---PLANKA_CARD---\s*(\{.*?\})\s*---END_CARD---", re.DOTALL
)


# Known team members: abbreviation/first name → full display name
_TEAM_MEMBERS = {
    "AP": "Angelos P",
    "AF": "Antonis Frs",
    "ML": "Marios L",
    "NT": "Nikos Tsaata",
    "angelos": "Angelos P",
    "antonis": "Antonis Frs",
    "marios": "Marios L",
    "nikos": "Nikos Tsaata",
}


def _build_planka_instruction(labels_str: str) -> str:
    members_str = (
        "AP/Angelos=dev&infra, AF/Antonis=dev&infra, "
        "ML/Marios=business&presentation, NT/Nikos=business&presentation"
    )
    return (
        "\n\n[ΟΔΗΓΙΑ ΣΥΣΤΗΜΑΤΟΣ - ΜΗΝ ΤΗΝ ΕΜΦΑΝΙΣΕΙΣ ΣΤΟΝ ΧΡΗΣΤΗ: "
        "Αν το μήνυμα περιγράφει task, feature, bug ή actionable ιδέα, "
        "πρόσθεσε στο ΤΕΛΟΣ της απάντησής σου αυτό το block:\n"
        "---PLANKA_CARD---\n"
        '{"title": "σύντιτλος max 80 χαρακτήρες", "description": "λεπτομέρειες", '
        f'"labels": ["επέλεξε 0-2 από: {labels_str} — χρησιμοποίησε τον ρόλο του μέλους ως hint"], '
        f'"assignee": "πλήρες όνομα αν αναφέρεται (αλλιώς null). Members: {members_str}"'
        "}\n"
        "---END_CARD---\n"
        "Αν είναι ερώτηση, χαιρετισμός ή casual συνομιλία, ΜΗΝ συμπεριλάβεις το block.]"
    )


async def _process_planka_block(response: str) -> tuple[str, str]:
    """Strip ---PLANKA_CARD--- block, create card, return (cleaned_response, confirmation)."""
    match = _PLANKA_BLOCK_RE.search(response)
    if not match:
        return response, ""
    cleaned = _PLANKA_BLOCK_RE.sub("", response).strip()
    try:
        card_data = json.loads(match.group(1))
        title = str(card_data.get("title", "Untitled"))[:80]
        description = str(card_data.get("description", ""))
        labels = card_data.get("labels", [])
        if not isinstance(labels, list):
            labels = []
        assignee_raw = card_data.get("assignee")
        # Normalize: treat the string "null" (AI output) as no assignee
        assignee = None
        if assignee_raw and str(assignee_raw).strip().lower() not in ("null", "none", ""):
            assignee = str(assignee_raw).strip()
            # Resolve abbreviation/first-name via _TEAM_MEMBERS mapping
            assignee = _TEAM_MEMBERS.get(assignee, _TEAM_MEMBERS.get(assignee.lower(), assignee))
        card = await _planka_client.create_card(title, description, labels, assignee_name=assignee)
        if card:
            assignee_note = f" → {assignee}" if assignee else ""
            logger.info(f"Planka card created: '{title}'{assignee_note} id={card.get('id')}")
            return cleaned, f"✅ Κάρτα: **{title}**{assignee_note}"
    except Exception as e:
        logger.warning(f"Planka block error: {e} | raw: {match.group(1)[:200]}")
    return cleaned, ""


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

# ── Planka Config ──────────────────────────────────────────────────────────────
PLANKA_URL       = os.getenv("PLANKA_URL", "")
PLANKA_BOARD_ID  = os.getenv("PLANKA_BOARD_ID", "")
PLANKA_EMAIL     = os.getenv("PLANKA_EMAIL", "")
PLANKA_PASSWORD  = os.getenv("PLANKA_PASSWORD", "")
PLANKA_LIST_NAME = os.getenv("PLANKA_LIST_NAME", "Test Card")

_planka_client = None
_planka_enabled = False

from vault_manager import VaultManager
from planka_client import PlankaClient

vm = VaultManager(VAULT_PATH)

CHANNELS_MAP = {
    "ideas": "meta/idea-dump",
    "decisions": "meta/decisions",
    "polls": "meta/polls",
    "questions": "meta/open-questions",
}

GITHUB_BASE = "https://github.com/dolly450/orderly_docs/blob/master"
FILES_FOLDERS = ["architecture", "design", "meta", "business", "pitch"]
OPENCODE_WEB_URL = "https://chat.haroldpoi.click/L2hvbWUvaGFyb2xkLy5vcGVuY2xhdy93b3Jrc3BhY2UvcHJvamVjdHMvb3JkZXJseV9kb2Nz"


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

    # Initialize Planka integration
    global _planka_client, _planka_enabled
    if PLANKA_URL and PLANKA_EMAIL and PLANKA_PASSWORD:
        _planka_client = PlankaClient(
            PLANKA_URL, PLANKA_BOARD_ID, PLANKA_EMAIL, PLANKA_PASSWORD, PLANKA_LIST_NAME
        )
        _planka_enabled = await _planka_client.initialize()
        logger.info(f"Planka {'enabled' if _planka_enabled else 'FAILED — card creation disabled'}")

    bot.loop.create_task(update_all_channels())
    bot.loop.create_task(_check_inactivity())

    bot.synced = True


async def _check_inactivity():
    """Every 30 s: reset session if chat has been idle for INACTIVITY_MINUTES."""
    global _last_activity
    while True:
        await asyncio.sleep(30)
        idle = datetime.utcnow() - _last_activity
        if idle > timedelta(minutes=INACTIVITY_MINUTES):
            logger.info(f"Inactivity ({int(idle.total_seconds()//60)} min) → creating new session")
            await _create_new_session()
            _last_activity = datetime.utcnow()
            for guild in bot.guilds:
                ch = discord.utils.get(guild.text_channels, name="chat")
                if ch:
                    await ch.send("🔄 *Context cleared due to inactivity — new session started.*")






async def update_files_channel():
    """Scan project folders and update the #files pinned message with categorized links."""
    for guild in bot.guilds:
        channel = discord.utils.get(guild.text_channels, name="files")
        if not channel:
            continue
        try:
            lines = ["📁 **Orderly Project Files**\n"]
            for folder in FILES_FOLDERS:
                folder_path = os.path.join(VAULT_PATH, folder)
                if not os.path.isdir(folder_path):
                    continue
                md_files = sorted(
                    f for f in os.listdir(folder_path) if f.endswith(".md")
                )
                if not md_files:
                    continue
                lines.append(f"\n**{folder}/**")
                for filename in md_files:
                    url = f"{GITHUB_BASE}/{folder}/{filename}"
                    lines.append(f"• [{filename}]({url})")
            lines.append(f"\n*Last Scan: {discord.utils.utcnow().strftime('%H:%M:%S UTC')}*")
            msg_text = "\n".join(lines)

            pins = await channel.pins()
            existing_pin = next((p for p in pins if p.author == bot.user), None)
            if existing_pin:
                await existing_pin.edit(content=msg_text)
            else:
                new_msg = await channel.send(msg_text)
                await new_msg.pin()
            logger.info("Updated #files channel pin")
        except Exception as e:
            logger.error(f"Error updating #files: {e}")


async def update_chat_info_pin():
    """Pin the OpenCode direct link in #chat."""
    for guild in bot.guilds:
        channel = discord.utils.get(guild.text_channels, name="chat")
        if not channel:
            continue
        try:
            msg_text = (
                "💬 **Orderly Chat**\n\n"
                "Μπορείτε επίσης να μιλήσετε απευθείας με το OpenCode από το παρακάτω link:\n"
                f"🔗 {OPENCODE_WEB_URL}"
            )
            pins = await channel.pins()
            existing_pin = next(
                (p for p in pins if p.author == bot.user and OPENCODE_WEB_URL in p.content),
                None
            )
            if existing_pin:
                await existing_pin.edit(content=msg_text)
            else:
                new_msg = await channel.send(msg_text)
                await new_msg.pin()
            logger.info("Updated #chat info pin")
        except Exception as e:
            logger.error(f"Error updating #chat pin: {e}")


async def update_all_channels():
    logger.info("Starting background vault sync...")
    for guild in bot.guilds:
        for channel_name, vault_topic in CHANNELS_MAP.items():
            channel = discord.utils.get(guild.text_channels, name=channel_name)
            if channel:
                await silent_update_channel(channel, vault_topic, channel_name.title())
                await asyncio.sleep(2)
    await update_files_channel()
    await update_chat_info_pin()
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
