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

class BettingView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    # Tlačítka, která hráči napoví příkaz
    @discord.ui.button(label="Koupit Sázka RED", style=discord.ButtonStyle.red)
    async def buy_red(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("👉 Napiš do chatu: `/item buy Sázka na Team Red`", ephemeral=True)

    @discord.ui.button(label="Koupit Sázka BLUE", style=discord.ButtonStyle.primary)
    async def buy_blue(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("👉 Napiš do chatu: `/item buy Sázka na Team Blue`", ephemeral=True)

@bot.event
async def on_ready():
    print('--- BOT JE READY ---')

@bot.event
async def on_message(message):
    if message.author.id == INHOUSE_BOT_ID:
        full_text = (message.content + " " + " ".join([e.title or "" for e in message.embeds]) + " " + " ".join([e.description or "" for e in message.embeds])).lower()
        
        if "game" in full_text and "starting" in full_text:
            channel = bot.get_channel(TARGET_CHANNEL_ID)
            if channel:
                await channel.send("💰 **Sázky otevřeny!**", view=BettingView())
                print("SÁZKA ODESLÁNA")

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
