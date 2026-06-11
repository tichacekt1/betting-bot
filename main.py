import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix="!", intents=intents)

INHOUSE_BOT_ID = 1001168331996409856

class BettingView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Vsadit RED", style=discord.ButtonStyle.red)
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("✅ Sázka na RED přijata!", ephemeral=True)

    @discord.ui.button(label="Vsadit BLUE", style=discord.ButtonStyle.primary)
    async def blue(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("✅ Sázka na BLUE přijata!", ephemeral=True)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} je připraven!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # DIAGNOSTIKA: Vypíše do terminálu každou zprávu, kterou bot vidí
    print(f"DEBUG: Zpráva od {message.author.id}: {message.content}")
    
    if message.author.id == INHOUSE_BOT_ID:
        obsah = message.content.lower()
        # Debug: vypíše, jestli bot detekoval start hry
        if "starting" in obsah or "found" in obsah:
            print("DEBUG: Detekován start hry, odesílám sázky...")
            try:
                await message.channel.send("💰 **Sázky otevřeny (10 min)!**", view=BettingView())
            except Exception as e:
                print(f"CHYBA při odesílání: {e}")
        else:
            print("DEBUG: Zpráva od InHouse bota ignorována (obsah nesouhlasí).")

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
