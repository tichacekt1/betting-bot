import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging

# Nastavení logování
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Definice bota a intentů
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    logger.info(f"Bot běží jako {bot.user}")

@bot.event
async def on_message(message):
    # Logování autora zprávy
    if message.author != bot.user:
        logger.info(f"Zpráva od {message.author.name} (ID: {message.author.id}) v kanálu #{message.channel}")

    # Kontrola zpráv od In House Queue bota (ID: 1001168331996409856)
    if message.author.id == 1001168331996409856:
        if message.embeds:
            embed = message.embeds[0]
            logger.info("!!! ZACHYCEN EMBED OD INHOUSE BOTA !!!")
            
            # Vypíše všechna pole, abychom viděli strukturu jmen hráčů
            for i, field in enumerate(embed.fields):
                logger.info(f"Field {i} - Název: {field.name} | Hodnota: {field.value}")
        else:
            logger.info("Zpráva od InHouse bota neobsahuje žádný Embed.")

    await bot.process_commands(message)

# Spuštění bota
token = os.getenv("DISCORD_TOKEN")
bot.run(token)
