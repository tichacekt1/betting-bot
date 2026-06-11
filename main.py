import discord
from discord.ext import commands
import os
import json
import asyncio
from dotenv import load_dotenv

# 1. NASTAVENÍ BOTA (Musí být na začátku)
load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

LOG_CHANNEL_ID = 1514649175931879455

# 2. POMOCNÉ FUNKCE
async def ukoncit_sazky(channel):
    await asyncio.sleep(600)
    await channel.send("🚫 **Sázky uzavřeny!** Čeká se na vyhlášení vítěze.")

async def vyhodnot_automaticky(channel, vitez):
    if not os.path.exists('sazky.json'):
        return
    with open('sazky.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    vitezove_text = f"🏆 **Zápas skončil! Vítězem je tým {vitez}!**\n\n**Výplatní listina:**\n"
    for user, saska in data.items():
        if saska['tym'] == vitez:
            vitezove_text += f"✅ {user}: vyhrál **{saska['castka']}**\n"
    await channel.send(vitezove_text)
    os.remove('sazky.json')

# 3. INTERAKCE (Tlačítka a Formulář)
class BettingModal(discord.ui.Modal, title='Vsadit na zápas'):
    castka = discord.ui.TextInput(label='Kolik chceš vsadit?', style=discord.TextStyle.short, required=True)
    def __init__(self, tym):
        super().__init__()
        self.tym = tym
    async def on_submit(self, interaction: discord.Interaction):
        data = {}
        if os.path.exists('sazky.json'):
            with open('sazky.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        data[interaction.user.name] = {"tym": self.tym, "castka": self.castka.value}
        with open('sazky.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        log_channel = interaction.guild.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(f"👤 **{interaction.user.name}** vsadil **{self.castka.value}** na tým **{self.tym}**.")
        await interaction.response.send_message(f"✅ Sázka uložena!", ephemeral=True)

class BettingView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=600)
    @discord.ui.button(label="Vsadit na RED", style=discord.ButtonStyle.red)
    async def red_bet(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(BettingModal("RED"))
    @discord.ui.button(label="Vsadit na BLUE", style=discord.ButtonStyle.primary)
    async def blue_bet(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(BettingModal("BLUE"))

# 4. UDÁLOSTI
@bot.event
async def on_ready():
    print(f'Bot je přihlášen jako {bot.user}')

@bot.event
async def on_message(message):
    if message.author.id == 1001168331996409856: # ID InHouse bota
        content = message.content.lower()
        if message.embeds and any("Red" in f.name or "Blue" in f.name for f in message.embeds[0].fields):
            await message.channel.send("💰 **Sázky otevřeny (10 min)!**", view=BettingView())
            bot.loop.create_task(ukoncit_sazky(message.channel))
        if "was declared winner!" in content:
            vitez = "RED" if "red team" in content else "BLUE"
            await vyhodnot_automaticky(message.channel, vitez)
    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
