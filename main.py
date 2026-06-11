import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# 1. NASTAVENÍ
load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

INHOUSE_BOT_ID = 1001168331996409856

# 2. TŘÍDY (UI prvky)
class BettingModal(discord.ui.Modal, title='Vsadit na zápas'):
    castka = discord.ui.TextInput(label='Kolik vsázíš?', style=discord.TextStyle.short, required=True)
    def __init__(self, tym):
        super().__init__()
        self.tym = tym
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"✅ Sázka {self.castka.value} na {self.tym} byla přijata.", ephemeral=True)

class BettingView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=600)
    @discord.ui.button(label="Vsadit RED", style=discord.ButtonStyle.red)
    async def red(self, interaction, button): await interaction.response.send_modal(BettingModal("RED"))
    @discord.ui.button(label="Vsadit BLUE", style=discord.ButtonStyle.primary)
    async def blue(self, interaction, button): await interaction.response.send_modal(BettingModal("BLUE"))

# 3. EVENTY (Logika bota)
@bot.event
async def on_ready():
    print(f'Bot {bot.user} je připraven a běží!')

@bot.event
async def on_message(message):
    # Ignoruj zprávy od bota samotného
    if message.author == bot.user:
        return
    
    # Detekce zpráv od InHouse bota
    if message.author.id == INHOUSE_BOT_ID:
        obsah = message.content.lower()
        # Přidáme kontrolu embedů
        for embed in message.embeds:
            if embed.description: obsah += " " + embed.description.lower()
        
        # Pokud se detekuje start hry
        if "game" in obsah and ("starting" in obsah or "found" in obsah):
            try:
                await message.channel.send("💰 **Sázky otevřeny (10 min)!**", view=BettingView())
            except discord.Forbidden:
                print("CHYBA: Bot nemá právo psát do tohoto kanálu!")
            except Exception as e:
                print(f"Neočekávaná chyba: {e}")

    await bot.process_commands(message)

# 4. SPUŠTĚNÍ
bot.run(os.getenv("DISCORD_TOKEN"))
