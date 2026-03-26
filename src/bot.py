import os
import discord
from discord import app_commands
from dotenv import load_dotenv
import requests

# Φόρτωση ρυθμίσεων
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
VAULT_PATH = os.getenv('VAULT_PATH')

# Εισαγωγή Vault Manager
from vault_manager import VaultManager
vm = VaultManager(VAULT_PATH)

# Χάρτης Καναλιών -> Αρχεία
CHANNELS_MAP = {
    'architecture': 'architecture/overview',
    'design': 'design/overview',
    'ordering-flow': 'architecture/ordering-flow',
    'ideas': 'meta/idea-dump',
    'decisions': 'meta/decisions',
    'questions': 'meta/open-questions'
}

class OrderlyBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

bot = OrderlyBot()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    
    for guild in bot.guilds:
        # 1. Δημιουργία/Ενημέρωση Καναλιών από το CHANNELS_MAP
        for channel_name, vault_topic in CHANNELS_MAP.items():
            channel = discord.utils.get(guild.text_channels, name=channel_name)
            if not channel:
                # Δημιουργία καναλιού αν δεν υπάρχει
                channel = await guild.create_text_channel(channel_name)
                print(f"Created new channel: #{channel_name}")
            
            await clean_and_update_channel(channel, vault_topic, channel_name.title())

        # 2. Δημιουργία καναλιού #chat αν δεν υπάρχει
        chat_channel = discord.utils.get(guild.text_channels, name='chat')
        if not chat_channel:
            chat_channel = await guild.create_text_channel('chat')
            print("Created #chat channel")
        
        await chat_channel.send("🤖 **Orderly AI Chat is Online!**\nΓράψτε οτιδήποτε εδώ για να με ρωτήσετε ή να συζητήσουμε για το project.")

async def clean_and_update_channel(channel, vault_topic, title):
    # Διαγραφή παλιών Pinned μηνυμάτων του bot
    pins = await channel.pins()
    for pin in pins:
        if pin.author == bot.user:
            await pin.delete()
            
    # Στέλνουμε το νέο μήνυμα
    content = vm.read_from_vault(vault_topic)
    github_link = f"https://github.com/dolly450/orderly_docs/blob/master/{vault_topic}.md"
    
    msg_text = (
        f"🚀 **Orderly Vault: {title}**\n"
        f"🔗 **Archive:** {github_link}\n\n"
        f"**Content:**\n```markdown\n{content}\n```"
    )
    
    new_msg = await channel.send(msg_text)
    await new_msg.pin()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Αν το μήνυμα είναι στο #chat, απαντάμε (Phase 2 Placeholder)
    if message.channel.name == 'chat':
        async with message.channel.typing():
            # Εδώ θα συνδέσουμε το OpenClaw κανονικά.
            # Για τώρα, μια έξυπνη απάντηση.
            response = f"Είμαι ο Orderly! Κατάλαβα το μήνυμά σου: '{message.content}'. Στο επόμενο βήμα θα μπορώ να αναλύω όλο το Vault για να σου απαντήσω!"
            await message.reply(response)

@bot.tree.command(name="idea", description="Καταγραφή ιδέας στο Idea Dump")
async def idea(interaction: discord.Interaction, text: str):
    await interaction.response.defer()
    user_name = interaction.user.global_name or interaction.user.name
    msg = vm.write_to_vault("meta/idea-dump", text, user_name)
    
    # Ενημέρωση του καναλιού #ideas αμέσως
    channel = discord.utils.get(interaction.guild.text_channels, name='ideas')
    if channel:
        await channel.send(f"💡 **Νέα Ιδέα από @{user_name}:** {text}")
        
    await interaction.followup.send(msg)

if __name__ == "__main__":
    bot.run(TOKEN)
