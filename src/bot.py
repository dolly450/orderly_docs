import os
import discord
from discord import app_commands
from dotenv import load_dotenv
import requests
import sys

# Φόρτωση ρυθμίσεων
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
VAULT_PATH = os.getenv('VAULT_PATH')
OPENCLAW_API = "http://localhost:11411/api/v1" # Το gateway URL του OpenClaw

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
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.tree.command(name="idea", description="Καταγραφή ιδέας στο Idea Dump")
async def idea(interaction: discord.Interaction, text: str):
    await interaction.response.defer()
    msg = vm.write_to_vault("meta/idea-dump", f"- {text}")
    await interaction.followup.send(msg)

@bot.tree.command(name="show", description="Εμφάνιση περιεχομένου από το Vault")
async def show(interaction: discord.Interaction, topic: str):
    content = vm.read_from_vault(topic)
    if len(content) > 1900:
        content = content[:1900] + "... (truncated)"
    await interaction.response.send_message(f"### Content for {topic}:\n```markdown\n{content}\n```")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Αν το μήνυμα είναι σε DM ή το bot γίνει mention, μιλάμε στο OpenClaw
    if isinstance(message.channel, discord.DMChannel) or bot.user.mentioned_in(message):
        async with message.channel.typing():
            # Καλούμε το OpenClaw (μέσω του Gateway)
            # ΣΗΜΕΙΩΣΗ: Εδώ θα μπορούσαμε να στείλουμε το μήνυμα στο sessions_send 
            # για να απαντήσω εγώ απευθείας.
            # Για το MVP, θα στείλουμε ένα placeholder και θα το συνδέσουμε στο Phase 2.
            response = f"Είμαι ο Orderly Bot! Δουλεύω με το OpenClaw για να βοηθήσω την ομάδα. (Phase 2 Integration incoming)"
            await message.reply(response)

if __name__ == "__main__":
    bot.run(TOKEN)
