import discord
from discord.ext import commands
import logging

# 1. Nastavení logování
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 2. Definice intentů (nutné pro čtení zpráv)
intents = discord.Intents.default()
intents.message_content = True

# 3. Definice bota (TOTO MUSÍ BÝT PŘED @bot.event)
bot = commands.Bot(command_prefix="!", intents=intents)

# 4. Třída pro sázková tlačítka
class BettingView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Vsadit na RED", style=discord.ButtonStyle.red)
    async def red_bet(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"{interaction.user.name} vsadil na RED!", ephemeral=True)

    @discord.ui.button(label="Vsadit na BLUE", style=discord.ButtonStyle.primary)
    async def blue_bet(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"{interaction.user.name} vsadil na BLUE!", ephemeral=True)

# 5. Hlavní události
@bot.event
async def on_ready():
    logger.info(f"Bot běží jako {bot.user}")

@bot.event
async def on_message(message):
    # Kontrola zpráv od In House Queue bota (ID 1001168331996409856)
    if message.author.id == 1001168331996409856 and message.embeds:
        embed = message.embeds[0]
        # Hledáme, jestli embed obsahuje týmy Red/Blue
        has_teams = any("Red" in field.name or "Blue" in field.name for field in embed.fields)
        
        if has_teams:
            await message.channel.send("💰 **Sázky otevřeny!** Kdo vyhraje tento zápas?", view=BettingView())

    await bot.process_commands(message)

# 6. Spuštění bota
# Ujisti se, že máš v souboru .env správný DISCORD_TOKEN
import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("DISCORD_TOKEN")
bot.run(token)
