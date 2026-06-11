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

# Událost při spuštění
@bot.event
async def on_ready():
    logger.info(f"Bot běží jako {bot.user}")

# Událost při zprávě
@bot.event
async def on_message(message):
    # Logování všeho, co bot vidí
    if message.author != bot.user:
        logger.info(f"Zpráva od {message.author} (ID: {message.author.id}) v kanálu #{message.channel}: {message.content[:50]}")
    
    await bot.process_commands(message)

# Spuštění bota
token = os.getenv("DISCORD_TOKEN")
bot.run(token)
