import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    logger.info(f"Bot běží jako {bot.user}")

@bot.event
async def on_message(message):
    # Logování každé zprávy, kterou bot vidí
    logger.info(f"Zpráva od {message.author} v kanálu #{message.channel}: {message.content[:50]}")
    
    # Pokud bot vidí zprávu od InHouse bota, vypíšeme detail
    if message.author.id == 1001168331996409856:
        logger.info(f"!!! ZACHYCENA ZPRÁVA OD INHOUSE BOTA !!!")
        logger.info(f"Embedy: {len(message.embeds)}")

    await bot.process_commands(message)

token = os.getenv("DISCORD_TOKEN")
bot.run(token)
