import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Nastavení
load_dotenv()
intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix="!", intents=intents)

INHOUSE_BOT_ID = 1001168331996409856

# Tlačítka pro sázky
class BettingView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) # Tlačítka zůstanou aktivní stále

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
    # Ignoruj zprávy od bota samotného
    if message.author == bot.user:
        return
    
    # Detekce zprávy od InHouse bota
    if message.author.id == INHOUSE_BOT_ID:
        obsah = message.content.lower()
        # Pokud se hra startuje, pošli tlačítka
        if "game" in obsah and ("starting" in obsah or "found" in obsah):
            try:
                await message.channel.send("💰 **Sázky otevřeny (10 min)!**", view=BettingView())
                print("Sázky úspěšně vypsány.")
            except discord.Forbidden:
                print("CHYBA: Bot nemá právo psát do tohoto kanálu!")

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
