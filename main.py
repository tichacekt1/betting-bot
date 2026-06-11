import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

INHOUSE_BOT_ID = 1001168331996409856
TARGET_CHANNEL_ID = 1507685027444555980
# Tvůj odkaz na obchod
STORE_URL = "https://unbelievaboat.com/dashboard/777881248949338123/store"

class BettingView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(label="Vsadit RED", style=discord.ButtonStyle.red, url=STORE_URL))
        self.add_item(discord.ui.Button(label="Vsadit BLUE", style=discord.ButtonStyle.primary, url=STORE_URL))

@bot.event
async def on_ready():
    print('--- BOT JE READY ---')

@bot.event
async def on_message(message):
    if message.author.id == INHOUSE_BOT_ID:
        full_text = (message.content + " " + " ".join([e.title or "" for e in message.embeds]) + " " + " ".join([e.description or "" for e in message.embeds])).lower()
        
        # Detekce startu hry
        if "game" in full_text and "starting" in full_text:
            channel = bot.get_channel(TARGET_CHANNEL_ID)
            if channel:
                await channel.send("💰 **Sázky otevřeny!**", view=BettingView())
                print("SÁZKA ODESLÁNA")

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
