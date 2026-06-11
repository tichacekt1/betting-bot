import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Načtení tokenu ze souboru .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ID botů a kanálů (tady máš ta svoje)
INHOUSE_BOT_ID = 1001168331996409856
BETTING_CHANNEL_ID = 1507685027444555980

@bot.event
async def on_ready():
    print(f'--- BĚŽÍ JAKO {bot.user} ---')

@bot.event
async def on_message(message):
    # Ignorujeme zprávy od sebe sama
    if message.author.id == bot.user.id:
        return

    # Sledujeme InHouse bota (hledáme začátek hry)
    if message.author.id == INHOUSE_BOT_ID:
        full_text = (message.content + " " + " ".join([e.title or "" for e in message.embeds]) + " " + " ".join([e.description or "" for e in message.embeds])).lower()
        
        if "game" in full_text and "starting" in full_text:
            channel = bot.get_channel(BETTING_CHANNEL_ID)
            if channel:
                # Odeslání zprávy s tlačítky pro obchod
                view = discord.ui.View()
                view.add_item(discord.ui.Button(label="Sázka RED", style=discord.ButtonStyle.red, url="https://unbelievaboat.com/dashboard/777881248949338123/store"))
                view.add_item(discord.ui.Button(label="Sázka BLUE", style=discord.ButtonStyle.primary, url="https://unbelievaboat.com/dashboard/777881248949338123/store"))
                
                await channel.send("💰 **Sázky otevřeny! Klikni a vsaď si v obchodu:**", view=view)
                print("SÁZKA ODESLÁNA")
            else:
                print(f"CHYBA: Nemůžu najít kanál {BETTING_CHANNEL_ID}")

    await bot.process_commands(message)

# Spuštění s načteným tokenem
bot.run(TOKEN)
