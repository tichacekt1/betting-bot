import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ID botů a kanálů
INHOUSE_BOT_ID = 1001168331996409856
BETTING_CHANNEL_ID = 1507685027444555980

@bot.event
async def on_ready():
    print('--- BOT JE READY ---')

@bot.event
async def on_message(message):
    # Ignorujeme zprávy od samotného bota
    if message.author.id == bot.user.id:
        return

    # Sledujeme zprávy od InHouse bota
    if message.author.id == INHOUSE_BOT_ID:
        print(f"DEBUG: Přišla zpráva od InHouse: {message.content[:50]}")
        
        # Hledáme klíčová slova startu
        if "game is starting" in message.content.lower():
            channel = bot.get_channel(BETTING_CHANNEL_ID)
            if channel:
                await channel.send("💰 **Sázky otevřeny!**")
                print("Sázka odeslána!")
            else:
                print("CHYBA: Nemůžu najít kanál pro sázky!")
    
    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
