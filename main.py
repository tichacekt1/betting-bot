import discord
from discord.ext import commands
import os
import json
import asyncio
import requests
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Konfigurace
LOG_CHANNEL_ID = 1514649175931879455
RESULTS_CHANNEL_ID = 1507869769787904040
INHOUSE_BOT_ID = 1001168331996409856
UB_TOKEN = os.getenv("UB_API_TOKEN")
UB_GUILD_ID = "292953664492929025"

class BettingModal(discord.ui.Modal, title='Vsadit na zápas'):
    castka = discord.ui.TextInput(label='Kolik vsázíš?', style=discord.TextStyle.short, required=True)
    def __init__(self, tym):
        super().__init__()
        self.tym = tym
    async def on_submit(self, interaction: discord.Interaction):
        # (Sem patří tvůj původní kód z BettingModal pro API volání)
        await interaction.response.send_message(f"✅ Sázka přijata!", ephemeral=True)

class BettingView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=600)
    @discord.ui.button(label="Vsadit RED", style=discord.ButtonStyle.red)
    async def red(self, interaction, button): await interaction.response.send_modal(BettingModal("RED"))
    @discord.ui.button(label="Vsadit BLUE", style=discord.ButtonStyle.primary)
    async def blue(self, interaction, button): await interaction.response.send_modal(BettingModal("BLUE"))

async def vyhodnot_automaticky(channel, vitez):
    # (Sem patří tvůj původní kód pro vyhodnocení)
    pass

@bot.event
async def on_message(message):
    if message.author == bot.user: return
    
    # Detekce zpráv od InHouse bota
    if message.author.id == INHOUSE_BOT_ID:
        content = message.content.lower()
        if "lobby" in content or "game was found" in content:
            await message.channel.send("💰 **Sázky otevřeny (10 min)!**", view=BettingView())
            
    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
