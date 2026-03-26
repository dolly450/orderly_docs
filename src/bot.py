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
        channel = discord.utils.get(guild.text_channels, name='ideas')
        if channel:
            content = vm.read_from_vault("meta/idea-dump")
            msg = f"🚀 **Orderly Vault: Idea Dump**\n\nLink: https://github.com/dolly450/orderly_docs/blob/master/meta/idea-dump.md\n\n**Ιδέες (Ιστορικό):**\n```markdown\n{content}\n```"
            sent_msg = await channel.send(msg)
            await sent_msg.pin()
            print(f"Pinned message to #{channel.name}")

@bot.tree.command(name="idea", description="Καταγραφή ιδέας στο Idea Dump")
async def idea(interaction: discord.Interaction, text: str):
    await interaction.response.defer()
    
    # Παίρνουμε το όνομα του χρήστη (global name ή username)
    user_name = interaction.user.global_name or interaction.user.name
    
    # Ενημέρωση του Vault με το όνομα του χρήστη
    msg = vm.write_to_vault("meta/idea-dump", text, user_name)
    
    # Ενημέρωση του καναλιού #ideas αμέσως
    channel = discord.utils.get(interaction.guild.text_channels, name='ideas')
    if channel:
        await channel.send(f"💡 **Νέα Ιδέα από @{user_name}:** {text}")
        
    await interaction.followup.send(msg)

@bot.tree.command(name="show", description="Εμφάνιση περιεχομένου από το Vault")
async def show(interaction: discord.Interaction, topic: str):
    content = vm.read_from_vault(topic)
    if len(content) > 1900:
        content = content[:1900] + "... (truncated)"
    await interaction.response.send_message(f"### Content for {topic}:\n```markdown\n{content}\n```")

if __name__ == "__main__":
    bot.run(TOKEN)
