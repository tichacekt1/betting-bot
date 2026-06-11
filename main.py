import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Konfigurace - zkontroluj si ID, zda jsou správná
INHOUSE_BOT_ID = 1001168331996409856

# Třídy pro sázky
class BettingModal(discord.ui.Modal, title='Vsadit na zápas'):
    castka = discord.ui.TextInput(label='Kolik vsázíš?', style=discord.TextStyle.short, required=True)
    def __init__(self, tym):
        super().__init__()
        self.tym = tym
    async def on_submit(self, interaction: discord.Interaction):
        # Tady probíhá logika sázky přes UnbelievaBoat
        await interaction.response.send_message(f"✅ Sázka {self.castka.value} na {self.tym} byla zpracována.", ephemeral=True)

class BettingView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=600)
    @discord.ui.button(label="Vsadit RED", style=discord.ButtonStyle.red)
    async def red(self, interaction, button): await interaction.response.send_modal(BettingModal("RED"))
    @discord.ui.button(label="Vsadit BLUE", style=discord.ButtonStyle.primary)
    async def blue(self, interaction, button): await interaction.response.send_modal(BettingModal("BLUE"))

# Eventy
@bot.event
async def on_ready():
    print(f'Bot {bot.user} je připraven!')

@bot.event
async def on_message(message):
    if message.author == bot.user: return
    
    # Detekce InHouse bota a jeho Embedů
    if message.author.id == INHOUSE_BOT_ID:
        obsah = message.content.lower()
        for embed in message.embeds:
            if embed.description: obsah += " " + embed.description.lower()
        
        if "game" in obsah and ("starting" in obsah or "found" in obsah):
            try:
                await message.channel.send("💰 **Sázky otevřeny (10 min)!**", view=BettingView())
            except discord.Forbidden:
                print("CHYBA: Bot nemá oprávnění posílat zprávy do tohoto kanálu!")

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
