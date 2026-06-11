import discord
from discord.ext import commands
import os
import logging
from dotenv import load_dotenv

# Nastavení
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Třída pro sázková tlačítka
class BettingView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) # Tlačítka zůstanou aktivní, dokud běží bot

    @discord.ui.button(label="Vsadit na RED", style=discord.ButtonStyle.red)
    async def red_bet(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Tady se v budoucnu napojí zápis do tvé databáze
        await interaction.response.send_message(f"✅ {interaction.user.name} vsadil na tým RED!", ephemeral=True)

    @discord.ui.button(label="Vsadit na BLUE", style=discord.ButtonStyle.primary)
    async def blue_bet(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Tady se v budoucnu napojí zápis do tvé databáze
        await interaction.response.send_message(f"✅ {interaction.user.name} vsadil na tým BLUE!", ephemeral=True)

@bot.event
async def on_ready():
    logger.info(f"Bot běží jako {bot.user}")

@bot.event
async def on_message(message):
    # Kontrola zpráv od In House Queue bota (ID 1001168331996409856)
    if message.author.id == 1001168331996409856 and message.embeds:
        embed = message.embeds[0]
        # Pokud embed obsahuje týmy Red/Blue, pošle sázkovou tabulku
        if any("Red" in field.name or "Blue" in field.name for field in embed.fields):
            try:
                await message.channel.send("💰 **Sázky otevřeny!** Kdo vyhraje tento zápas?", view=BettingView())
            except discord.Forbidden:
                logger.error(f"Stále nemám práva psát do kanálu #{message.channel.name}!")

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
