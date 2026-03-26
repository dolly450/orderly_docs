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

async def get_ai_response(vm_instance, user_name, user_question):
    OPENCLAW_CMD = os.getenv('OPENCLAW_PATH', '/home/harold/.bun/bin/openclaw')
    ideas = await asyncio.to_thread(vm_instance.read_from_vault, 'meta/idea-dump')
    questions = await asyncio.to_thread(vm_instance.read_from_vault, 'meta/open-questions')
    arch = await asyncio.to_thread(vm_instance.read_from_vault, 'architecture/overview')
    context = f"Ideas: {ideas[:200]}\nQuestions: {questions[:200]}\nArchitecture: {arch[:200]}"
    full_prompt = f"Vault Context: {context}\n\nUser (@{user_name}) asks: {user_question}\n\nAnswer briefly."
    process = await asyncio.create_subprocess_exec(
        OPENCLAW_CMD, 'ask', full_prompt,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    if process.returncode == 0:
        return stdout.decode().strip()
    else:
        raise Exception(stderr.decode())

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
        content = ""
        if vault_topic == "meta/polls":
            # Handle JSON polls
            file_path = os.path.join(VAULT_PATH, "meta/polls.json")
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
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
        
        github_link = f"https://github.com/dolly450/orderly_docs/blob/master/{vault_topic}.md"
        if vault_topic == "meta/polls":
             github_link = f"https://github.com/dolly450/orderly_docs/blob/master/meta/polls.json"
        
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
                response = await get_ai_response(vm, message.author.name, message.content)
                if response: await message.reply(response[:1900])
            except Exception as e:
                logger.error(f"Chat error: {e}")

@bot.tree.command(name="idea", description="Καταγραφή ιδέας")
async def idea(interaction: discord.Interaction, text: str):
    await interaction.response.defer()
    user_name = interaction.user.global_name or interaction.user.name
    try:
        result_msg = await asyncio.to_thread(process_idea_command, vm, text, user_name)
        await interaction.followup.send(result_msg)
        
        # Update ONLY the dedicated #ideas channel
        dedicated_channel = discord.utils.get(interaction.guild.text_channels, name="ideas")
        if dedicated_channel:
            bot.loop.create_task(silent_update_channel(dedicated_channel, "meta/idea-dump", "Idea Dump"))
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
        result_msg = await asyncio.to_thread(process_question_command, vm, text, user_name)
        await interaction.followup.send(result_msg)
        
        # Update ONLY the dedicated #questions channel
        dedicated_channel = discord.utils.get(interaction.guild.text_channels, name="questions")
        if dedicated_channel:
            bot.loop.create_task(silent_update_channel(dedicated_channel, "meta/open-questions", "Questions"))
        else:
            logger.warning("Dedicated #questions channel not found for pinning.")
            
    except Exception as e:
        logger.error(f"Question command error: {e}")
        await interaction.followup.send("Failed to log question due to an internal error.")

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
        dedicated_channel = discord.utils.get(interaction.guild.text_channels, name="polls")
        if dedicated_channel:
            bot.loop.create_task(silent_update_channel(dedicated_channel, "meta/polls", "Polls"))
        else:
            logger.warning("Dedicated #polls channel not found for pinning.")
        
        # Add initial reaction
        await poll_msg.add_reaction('✅')
    except Exception as e:
        logger.error(f"Poll command error: {e}")
        await interaction.followup.send("Failed to log poll due to an internal error.")

@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:
        return
        
    if payload.emoji.name == '✅':
        channel = bot.get_channel(payload.channel_id)
        if not channel: return
        
        try:
            msg = await channel.fetch_message(payload.message_id)
            if msg.author == bot.user and "📊 **Poll by" in msg.content and "(ID: `poll-" in msg.content:
                # Extract poll ID
                import re
                match = re.search(r"\(ID: `(poll-\d+)`\)", msg.content)
                if not match: return
                poll_id = match.group(1)
                
                # Sync vote to JSON
                user_id = str(payload.user_id)
                await asyncio.to_thread(vm.add_vote, poll_id, user_id)
                
                # Check threshold (using reaction count is safer as it represents current state)
                for reaction in msg.reactions:
                    if str(reaction.emoji) == '✅' and reaction.count >= 4:
                        # Threshold reached! Archive it
                        await asyncio.to_thread(vm.archive_poll, poll_id)
                        
                        # Delete the discord poll message
                        await msg.delete()
                        
                        # Update pins for both polls and decisions
                        polls_channel = discord.utils.get(channel.guild.text_channels, name='polls')
                        if polls_channel:
                            bot.loop.create_task(silent_update_channel(polls_channel, "meta/polls", "Polls"))
                            
                        decisions_channel = discord.utils.get(channel.guild.text_channels, name='decisions')
                        if decisions_channel:
                            bot.loop.create_task(silent_update_channel(decisions_channel, "meta/decisions", "Decisions"))
                        break
                else:
                    # Just update the polls pin to show new vote count
                    polls_channel = discord.utils.get(channel.guild.text_channels, name='polls')
                    if polls_channel:
                        bot.loop.create_task(silent_update_channel(polls_channel, "meta/polls", "Polls"))
                        
        except Exception as e:
            logger.error(f"Reaction handler error: {e}")

if __name__ == "__main__":
    if not TOKEN:
        logger.error("NO DISCORD_TOKEN FOUND IN .ENV!")
    else:
        bot.run(TOKEN)
