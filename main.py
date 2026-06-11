import discord
from discord.ext import commands
import os
import json
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Funkce pro uložení sázky
def uloz_sazku(uzivatel, tym, castka):
    data = {}
    if os.path.exists('sazky.json'):
        with open('sazky.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    
    data[uzivatel] = {"tym": tym, "castka": castka}
    with open('sazky.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

# Formulář pro zadání částky
class BettingModal(discord.ui.Modal, title='Vsadit na zápas'):
    castka = discord.ui.TextInput(label='Kolik chceš vsadit?', style=discord.TextStyle.short, required=True)

    def __init__(self, tym):
        super().__init__()
        self.tym = tym

    async def on_submit(self, interaction: discord.Interaction):
        uloz_sazku(interaction.user.name, self.tym, self.castka.value)
        await interaction.response.send_message(f"✅ Sázka {self.castka.value} na {self.tym} uložena!", ephemeral=True)

# Tlačítka
class BettingView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Vsadit na RED", style=discord.ButtonStyle.red, custom_id="red_button")
    async def red_bet(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(BettingModal("RED"))

    @discord.ui.button(label="Vsadit na BLUE", style=discord.ButtonStyle.primary, custom_id="blue_button")
    async def blue_bet(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(BettingModal("BLUE"))

@bot.event
async def on_message(message):
    if message.author.id == 1001168331996409856 and message.embeds:
        if any("Red" in f.name or "Blue" in f.name for f in message.embeds[0].fields):
            await message.channel.send("💰 **Sázky otevřeny!** Klikni na tlačítko a zadej částku:", view=BettingView())
    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
