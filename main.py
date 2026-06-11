import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging

# 1. Nastavení
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 2. Definice bota (TOTO MUSÍ BÝT PŘED @bot.event)
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 3. Události
@bot.event
async def on_ready():
    logger.info(f"Bot běží jako {bot.user}")

@bot.event
async def on_message(message):
    # Logování autora
    if message.author != bot.user:
        logger.info(f"Zpráva od {message.author.name} (ID: {message.author.id}) v kanálu #{message.channel}: {message.content[:50]}")
    
    # 4. Tady je to propojení s ID InHouse bota
    # Podle tvého posledního screenshotu je ID InHouse bota 1001168331996409856
    if message.author.id == 1001168331996409856:
        logger.info("!!! ZACHYCENA ZPRÁVA OD INHOUSE BOTA !!!")
        # Zde později přidáme volání tvé funkce pro sázku

    await bot.process_commands(message)

# 5. Spuštění
token = os.getenv("DISCORD_TOKEN")
bot.run(token)
