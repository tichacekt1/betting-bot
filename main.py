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

# Konfigurace - ZKONTROLUJ SI TYTO ID, ZDA JSOU SPRÁVNÉ!
LOG_CHANNEL_ID = 1514649175931879455
RESULTS_CHANNEL_ID = 1507869769787904040
INHOUSE_BOT_ID = 1001168331996409856 # Ujisti se, že tohle je ID bota, co píše ty zprávy
UB_TOKEN = os.getenv("UB_API_TOKEN")
UB_GUILD_ID = "292953664492929025"

# --- Zbytek tříd BettingModal a BettingView nechej tak, jak je máš, jsou v pořádku ---
# (Sem vlož své původní BettingModal a BettingView)

@bot.event
async def on_ready():
    print(f'Bot je přihlášen jako {bot.user}')

@bot.event
async def on_message(message):
    # Ignoruj zprávy od sebe sama
    if message.author == bot.user:
        return

    # Debug: když bot vidí jakoukoli zprávu, vypíše to do konzole (pomůže nám to diagnostikovat)
    print(f"Nová zpráva od {message.author.name} (ID: {message.author.id}): {message.content[:50]}")

    # Logika pro automatické vyhodnocení
    # Přidána podmínka 'or message.author.id == 0' pokud je to webhook
    if message.author.id == INHOUSE_BOT_ID or message.author.bot: 
        content = message.content.lower()
        
        # Detekce vítěze
        if "winner" in content or "declared winner" in content:
            vitez = "RED" if "red" in content else "BLUE"
            await vyhodnot_automaticky(message.channel, vitez)
            return

        # Detekce vytvoření lobby (zjednodušeno, aby reagoval snadněji)
        if "lobby" in content or (message.embeds and "game" in str(message.embeds[0].to_dict()).lower()):
            try:
                await message.channel.send("💰 **Sázky otevřeny (10 min)!**", view=BettingView())
            except discord.Forbidden:
                print("Chyba: Bot nemá oprávnění posílat zprávy!")

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
