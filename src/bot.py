import os
import re
import json
import subprocess
import fcntl
import sys
import discord
from discord import app_commands
from dotenv import load_dotenv
import asyncio
import logging
from datetime import datetime, timedelta
import collections
from check_claude_quota import get_quota_string, get_quota_reset_datetime
# ── Single-instance lock ──────────────────────────────────────────────────────
_LOCK_FILE = "/tmp/orderly-bot.lock"
_lock_fd = None

def _enforce_singleton():
    import signal, time
    old_pid = None
    if os.path.exists(_LOCK_FILE):
        try:
            with open(_LOCK_FILE, "r") as f:
                old_pid = int(f.read().strip())
        except Exception:
            pass

    fd = open(_LOCK_FILE, "a")
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        if old_pid:
            print(f"orderly-bot already running (PID {old_pid}). Killing it to take over...", flush=True)
            try:
                os.kill(old_pid, signal.SIGTERM)
                time.sleep(1)
            except Exception:
                pass
            
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except IOError:
                print("Failed to acquire lock after killing old PID. Exiting with error.", flush=True)
                sys.exit(1)
        else:
            print("orderly-bot already running but couldn't find PID. Exiting with error.", flush=True)
            sys.exit(1)
            
    # Now we own the lock, overwrite it with our PID.
    fd.close()
    
    fd = open(_LOCK_FILE, "w")
    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    fd.write(str(os.getpid()))
    fd.flush()
    return fd

if "pytest" not in sys.modules:
    _lock_fd = _enforce_singleton()
else:
    _lock_fd = None

# Ρύθμιση Logging σε ΑΡΧΕΙΟ
log_file = "/home/harold/.openclaw/workspace/projects/orderly_docs/orderly_bot.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
)
logger = logging.getLogger("OrderlyBot")

# ── Claude CLI Config ─────────────────────────────────────────────────────────
CLAUDE_BIN       = "/home/harold/.local/bin/claude"
SESSION_FILE     = os.path.join(os.path.dirname(__file__), "..", "claude_session.json")
SESSION_TTL_MIN  = 60
PROJECT_DIR      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_HAIKU      = "claude-haiku-4-5-20251001"
MODEL_SONNET     = "claude-sonnet-4-6"
COMPLEX_KEYWORDS = {
    "implement", "build", "analyze", "plan", "debug", "fix", "create", "refactor",
    "design", "architect", "εφαρμογή", "ανάλυση", "υλοποίηση", "δημιουργία", "σχεδίαση",
}

# ── Gemini CLI Config ─────────────────────────────────────────────────────────
GEMINI_BIN       = "gemini"
GEMINI_SESSION_FILE = os.path.join(os.path.dirname(__file__), "..", "gemini_session.json")

# Shared mutable state
_session_id    = None   # str | None
_session_start = None   # datetime | None
_gemini_session_id = None
_gemini_session_start = None

_fallback_until_dt = None
_active_provider = "claude"
_chat_history_buffer = collections.deque(maxlen=6)


# ── Claude CLI helpers ────────────────────────────────────────────────────────

def _select_model(text: str) -> str:
    """Choose Haiku for short/simple messages, Sonnet for complex ones."""
    if len(text) < 150 and not any(kw in text.lower() for kw in COMPLEX_KEYWORDS):
        return MODEL_HAIKU
    return MODEL_SONNET


def _load_session() -> tuple:
    """Load session state from disk. Returns (session_id, session_start) or (None, None)."""
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE) as f:
                data = json.load(f)
            return data["session_id"], datetime.fromisoformat(data["session_start"])
        except Exception:
            pass
    return None, None


def _save_session(session_id: str, session_start: datetime) -> None:
    with open(SESSION_FILE, "w") as f:
        json.dump({"session_id": session_id, "session_start": session_start.isoformat()}, f)

def _load_gemini_session() -> tuple:
    if os.path.exists(GEMINI_SESSION_FILE):
        try:
            with open(GEMINI_SESSION_FILE) as f:
                data = json.load(f)
            return data["session_id"], datetime.fromisoformat(data["session_start"])
        except Exception:
            pass
    return None, None

def _save_gemini_session(session_id: str, session_start: datetime) -> None:
    with open(GEMINI_SESSION_FILE, "w") as f:
        json.dump({"session_id": session_id, "session_start": session_start.isoformat()}, f)


def _get_git_diff(pre_hash: str) -> str:
    """Return git diff since pre_hash, truncated to 800 chars."""
    try:
        post = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=PROJECT_DIR, capture_output=True, text=True
        ).stdout.strip()
        if post and post != pre_hash:
            diff_cmd = ["git", "diff", f"{pre_hash}..HEAD"]
        else:
            diff_cmd = ["git", "diff", "HEAD"]
        result = subprocess.run(diff_cmd, cwd=PROJECT_DIR, capture_output=True, text=True)
        diff = result.stdout.strip()
        if len(diff) > 800:
            diff = diff[:780] + "\n... (truncated)"
        return diff
    except Exception:
        return ""


def _format_diff_block(diff: str, budget: int) -> str:
    header = "\n📝 **Αλλαγές:**\n```diff\n"
    footer = "\n```"
    available = budget - len(header) - len(footer)
    if available <= 50:
        return ""
    if len(diff) > available:
        diff = diff[:available - 20] + "\n... (truncated)"
    return header + diff + footer


async def _send_claude_chat(user_name: str, text: str) -> str:
    """Run claude CLI headlessly and return the response, with optional git diff block."""
    global _session_id, _session_start

    model = _select_model(text)
    now = datetime.utcnow()

    session_valid = (
        _session_id is not None
        and _session_start is not None
        and (now - _session_start) < timedelta(minutes=SESSION_TTL_MIN)
    )
    if not session_valid and _session_id is not None:
        age_min = int((now - _session_start).total_seconds() // 60) if _session_start else "?"
        logger.info(f"Session {_session_id} expired after {age_min} min — starting fresh")

    planka_suffix = ""
    if _planka_enabled and _planka_client:
        labels_str = ", ".join(f'"{n}"' for n in _planka_client.get_label_names())
        planka_suffix = _build_planka_instruction(labels_str)

    full_msg = f"{user_name}: {text}{planka_suffix}"

    cmd = [CLAUDE_BIN, "--print", "--dangerously-skip-permissions", "--output-format", "json", "--model", model]
    if session_valid:
        cmd += ["--resume", _session_id]
    cmd.append(full_msg)

    pre_hash = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=PROJECT_DIR, capture_output=True, text=True
    ).stdout.strip()

    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=PROJECT_DIR,
        )
        stdout_b, stderr_b = await asyncio.wait_for(proc.communicate(), timeout=120)
    except asyncio.TimeoutError:
        return "⚠️ Claude CLI timeout — check logs."

    if proc.returncode != 0:
        logger.error(f"claude exited {proc.returncode}: {stderr_b.decode()[:300]}")
        quota_msg = await asyncio.to_thread(get_quota_string)
        return f"⚠️ Claude CLI error — likely hit Claude API quota limit. Check logs.\n\n```text\n{quota_msg}\n```"
    try:
        data = json.loads(stdout_b.decode())
    except Exception as e:
        logger.error(f"Claude JSON parse error: {e} | raw: {stdout_b[:200]}")
        return "⚠️ Claude returned unexpected output."

    if data.get("is_error"):
        quota_msg = await asyncio.to_thread(get_quota_string)
        return f"⚠️ Claude CLI error: {data.get('result', 'unknown error')[:200]} — likely hit Claude API quota limit. Check logs.\n\n```text\n{quota_msg}\n```"

    # Update session state
    new_id = data.get("session_id")
    if new_id:
        _session_id = new_id
        if not session_valid:
            _session_start = now
        _save_session(_session_id, _session_start)
        logger.info(f"Claude session: {_session_id} (model: {model})")

    response = data.get("result", "").strip()

    # Append git diff if files changed
    diff_str = await asyncio.to_thread(_get_git_diff, pre_hash)
    if diff_str:
        diff_block = _format_diff_block(diff_str, 1900 - len(response))
        response = response + diff_block

    if len(response) > 1900:
        response = response[:1900] + "... (truncated)"

    return response or "⚠️ Claude returned an empty response."


async def _send_gemini_chat(user_name: str, text: str) -> str:
    """Run gemini CLI headlessly and return the response."""
    global _gemini_session_id, _gemini_session_start

    now = datetime.utcnow()
    session_valid = (
        _gemini_session_id is not None
        and _gemini_session_start is not None
        and (now - _gemini_session_start) < timedelta(minutes=SESSION_TTL_MIN)
    )

    planka_suffix = ""
    if _planka_enabled and _planka_client:
        labels_str = ", ".join(f'"{n}"' for n in _planka_client.get_label_names())
        planka_suffix = _build_planka_instruction(labels_str)

    full_msg = f"{user_name}: {text}{planka_suffix}"

    cmd = [GEMINI_BIN, "-p", full_msg, "--output-format", "json"]
    if session_valid:
        cmd += ["--resume", _gemini_session_id]

    pre_hash = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=PROJECT_DIR, capture_output=True, text=True
    ).stdout.strip()

    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=PROJECT_DIR,
        )
        stdout_b, stderr_b = await asyncio.wait_for(proc.communicate(), timeout=120)
    except asyncio.TimeoutError:
        return "⚠️ Gemini CLI timeout — check logs."

    if proc.returncode != 0:
        logger.error(f"gemini exited {proc.returncode}: {stderr_b.decode()[:300]}")
        return f"⚠️ Gemini CLI error. Check logs.\n\n```text\n{stderr_b.decode()[:300]}\n```"
    try:
        data = json.loads(stdout_b.decode())
    except Exception as e:
        logger.error(f"Gemini JSON parse error: {e} | raw: {stdout_b[:200]}")
        return "⚠️ Gemini returned unexpected output."

    new_id = data.get("session_id")
    if new_id:
        _gemini_session_id = new_id
        if not session_valid:
            _gemini_session_start = now
        _save_gemini_session(_gemini_session_id, _gemini_session_start)
        logger.info(f"Gemini session: {_gemini_session_id}")

    response = data.get("result", "").strip()

    diff_str = await asyncio.to_thread(_get_git_diff, pre_hash)
    if diff_str:
        diff_block = _format_diff_block(diff_str, 1900 - len(response))
        response = response + diff_block

    if len(response) > 1900:
        response = response[:1900] + "... (truncated)"

    return response or "⚠️ Gemini returned an empty response."


async def _send_chat(user_name: str, text: str) -> str:
    global _fallback_until_dt, _active_provider, _chat_history_buffer
    now = datetime.utcnow()

    # Check if fallback expired
    if _fallback_until_dt and now > _fallback_until_dt:
        logger.info("Fallback timer expired. Returning to Claude.")
        _fallback_until_dt = None

    target_provider = "gemini" if _fallback_until_dt else "claude"
    
    # Context handoff injection
    handoff_text = text
    if target_provider != _active_provider and len(_chat_history_buffer) > 0:
        history_str = "\n".join(f"{u}: {m}" for u, m in _chat_history_buffer)
        handoff_text = f"<context_handoff>\n{history_str}\n</context_handoff>\n\nUser: {text}"
        _active_provider = target_provider

    if target_provider == "claude":
        response = await _send_claude_chat(user_name, handoff_text)
        
        # Detect Claude quota hit
        if "hit Claude API quota limit" in response or "rate_limit_error" in response:
            reset_dt = await asyncio.to_thread(get_quota_reset_datetime)
            if reset_dt and reset_dt > now:
                _fallback_until_dt = reset_dt
            else:
                _fallback_until_dt = now + timedelta(hours=1)
                
            logger.warning(f"Claude quota hit. Falling back to Gemini until {_fallback_until_dt}")
            
            target_provider = "gemini"
            _active_provider = "gemini"
            
            if len(_chat_history_buffer) > 0:
                history_str = "\n".join(f"{u}: {m}" for u, m in _chat_history_buffer)
                handoff_text = f"<context_handoff>\n{history_str}\n</context_handoff>\n\nUser: {text}"
            else:
                handoff_text = text
                
            gemini_response = await _send_gemini_chat(user_name, handoff_text)
            
            _chat_history_buffer.append((user_name, text))
            _chat_history_buffer.append(("AI", gemini_response))
            return gemini_response

        _chat_history_buffer.append((user_name, text))
        _chat_history_buffer.append(("AI", response))
        return response
    
    else:
        response = await _send_gemini_chat(user_name, handoff_text)
        _chat_history_buffer.append((user_name, text))
        _chat_history_buffer.append(("AI", response))
        return response


# ── Planka helpers ────────────────────────────────────────────────────────────

def _build_planka_instruction(labels_str: str) -> str:
    vault = os.getenv("VAULT_PATH", "/home/harold/.openclaw/workspace/projects/orderly_docs")
    members_str = (
        "AP/Angelos P (dev&infra), AF/Antonis Frs (dev&infra), "
        "ML/Marios L (business), NT/Nikos Tsaata (business)"
    )
    return (
        f"\n\n[ΟΔΗΓΙΑ ΣΥΣΤΗΜΑΤΟΣ - ΜΗΝ ΤΗΝ ΕΜΦΑΝΙΣΕΙΣ ΣΤΟΝ ΧΡΗΣΤΗ: "
        f"Αν το μήνυμα περιγράφει task, feature, bug ή actionable ιδέα, "
        f"τρέξε ΑΜΕΣΩΣ την παρακάτω εντολή (μία κάρτα μόνο):\n"
        f"  cd {vault} && python src/planka_create.py "
        f'--title "σύντιτλος max 80 χαρ" '
        f'--description "λεπτομέρειες" '
        f'--labels "label1,label2" '
        f'--assignee "συντομογραφία ή όνομα"\n'
        f"Διαθέσιμα labels: {labels_str}\n"
        f"Members: {members_str}\n"
        f"Αν είναι ερώτηση ή casual chat, ΜΗΝ τρέξεις την εντολή.\n"
        f"ΠΑΝΤΑ απάντα στα ΕΛΛΗΝΙΚΆ, ακόμα και αν το μήνυμα είναι στα αγγλικά.]"
    )


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

    # Load existing Claude session if available
    global _session_id, _session_start
    _session_id, _session_start = _load_session()
    if _session_id:
        logger.info(f"Loaded existing Claude session: {_session_id}")
    else:
        logger.info("No existing Claude session — will create on first message")

    global _gemini_session_id, _gemini_session_start
    _gemini_session_id, _gemini_session_start = _load_gemini_session()
    if _gemini_session_id:
        logger.info(f"Loaded existing Gemini session: {_gemini_session_id}")

    # Initialize Planka integration
    global _planka_client, _planka_enabled
    if PLANKA_URL and PLANKA_EMAIL and PLANKA_PASSWORD:
        _planka_client = PlankaClient(
            PLANKA_URL, PLANKA_BOARD_ID, PLANKA_EMAIL, PLANKA_PASSWORD, PLANKA_LIST_NAME
        )
        _planka_enabled = await _planka_client.initialize()
        logger.info(f"Planka {'enabled' if _planka_enabled else 'FAILED — card creation disabled'}")

    bot.loop.create_task(update_all_channels())

    bot.synced = True






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
    """Pin usage info in #chat."""
    for guild in bot.guilds:
        channel = discord.utils.get(guild.text_channels, name="chat")
        if not channel:
            continue
        try:
            msg_text = (
                "💬 **Orderly Chat**\n\n"
                "Μιλήστε με τον Claude agent εδώ.\n"
                "Haiku → σύντομα ερωτήματα | Sonnet → σύνθετα/τεχνικά\n"
                "Session καθαρίζεται μετά από 60 λεπτά."
            )
            pins = await channel.pins()
            existing_pin = next(
                (p for p in pins if p.author == bot.user and "Orderly Chat" in p.content),
                None,
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
        async with message.channel.typing():
            try:
                response = await _send_chat(
                    message.author.global_name or message.author.name,
                    message.content,
                )
                await message.reply(response)
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
