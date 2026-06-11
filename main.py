import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True  # Toto je klíčové
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print('--- BOT JE READY ---')

@bot.event
async def on_message(message):
    # Vypiš VŠECHNO, co bot vidí
    print(f"DEBUG: Zpráva v kanálu {message.channel.name} od {message.author.name}: {message.content[:50]}")
    
    # Kód pro odeslání sázek, pokud to napíše InHouse bot
    if message.author.id == 1001168331996409856:
        print("DEBUG: NAŠEL JSEM INHOUSE BOTA!")
        if "game is starting" in message.content.lower():
            channel = bot.get_channel(1507685027444555980)
            if channel:
                await channel.send("💰 **Sázky otevřeny!**")
                print("Sázka odeslána!")
            else:
                print("CHYBA: Nemůžu najít kanál 1507685027444555980!")

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
