import os
import discord
from discord import app_commands
from dotenv import load_dotenv
import asyncio
import logging
import subprocess
from datetime import datetime

# Ρύθμιση Logging σε ΑΡΧΕΙΟ
log_file = "/home/harold/.openclaw/workspace/projects/orderly_docs/orderly_bot.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('OrderlyBot')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
VAULT_PATH = os.getenv('VAULT_PATH')

from vault_manager import VaultManager
vm = VaultManager(VAULT_PATH)

CHANNELS_MAP = {
    'architecture': 'architecture/overview',
    'design': 'design/overview',
    'ordering-flow': 'architecture/ordering-flow',
    'ideas': 'meta/idea-dump',
    'decisions': 'meta/decisions',
    'polls': 'meta/polls',
    'questions': 'meta/open-questions'
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
        try:
            await self.tree.sync()
            logger.info("Slash Commands Synced!")
        except Exception as e:
            logger.error(f"Error syncing commands: {e}")

bot = OrderlyBot()

@bot.event
async def on_ready():
    if bot.synced:
        return
    logger.info(f'SUCCESS: Logged in as {bot.user} (ID: {bot.user.id})')
    bot.loop.create_task(update_all_channels())
    bot.synced = True

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
        content = vm.read_from_vault(vault_topic)
        github_link = f"https://github.com/dolly450/orderly_docs/blob/master/{vault_topic}.md"
        
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
    if message.channel.name == 'chat':
        async with message.channel.typing():
            try:
                context = f"Vault Context: {vm.read_from_vault('meta/idea-dump')[:300]}"
                full_prompt = f"{context}\n\nUser (@{message.author.name}) asks: {message.content}\n\nAnswer briefly."
                process = await asyncio.create_subprocess_exec(
                    'openclaw', 'ask', full_prompt,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await process.communicate()
                if process.returncode == 0:
                    response = stdout.decode().strip()
                    if response: await message.reply(response[:1900])
                else:
                    logger.error(f"AI Error: {stderr.decode()}")
            except Exception as e:
                logger.error(f"Chat error: {e}")

@bot.tree.command(name="idea", description="Καταγραφή ιδέας")
async def idea(interaction: discord.Interaction, text: str):
    await interaction.response.defer()
    user_name = interaction.user.global_name or interaction.user.name
    vm.write_to_vault("meta/idea-dump", text, user_name)
    await interaction.followup.send(f"💡 Idea added!")
    bot.loop.create_task(silent_update_channel(interaction.channel, "meta/idea-dump", "Idea Dump"))

if __name__ == "__main__":
    if not TOKEN:
        logger.error("NO DISCORD_TOKEN FOUND IN .ENV!")
    else:
        bot.run(TOKEN)
