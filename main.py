import discord
from discord.ext import commands
import os
import json
import asyncio
from dotenv import load_dotenv

# --- KONFIGURACE ---
load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ID kanálů
LOG_CHANNEL_ID = 1514649175931879455    # Kanál pro logování sázek
RESULTS_CHANNEL_ID = 1507869769787904040 # Kanál pro výsledky
INHOUSE_BOT_ID = 1001168331996409856    # ID InHouse bota

# --- POMOCNÉ FUNKCE ---
async def ukoncit_sazky(channel):
    await asyncio.sleep(600)  # Čekání 10 minut
    await channel.send("🚫 **Sázky uzavřeny!** Čeká se na vyhlášení vítěze.")

async def vyhodnot_automaticky(channel, vitez):
    if not os.path.exists('sazky.json'):
        return
    
    with open('sazky.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    results_channel = channel.guild.get_channel(RESULTS_CHANNEL_ID)
    if not results_channel:
        await channel.send("❌ Chyba: Kanál pro výsledky nebyl nalezen!")
        return

    vitezove_text = f"🏆 **Zápas skončil! Vítězem je tým {vitez}!**\n\n**Výplatní listina:**\n"
    vyhry = False
    for user, saska in data.items():
        if saska['tym'] == vitez:
            vitezove_text += f"✅ {user}: vyhrál **{saska['castka']}**\n"
            vyhry = True
    
    if not vyhry:
        vitezove_text += "Nikdo nevsadil na vítězný tým."
    
    await results_channel.send(vitezove_text)
    os.remove('sazky.json')
    await channel.send("✅ Výsledky byly odeslány do kanálu pro výsledky.")

# --- INTERAKCE (Tlačítka a Formulář) ---
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

# --- UDÁLOSTI ---
@bot.event
async def on_ready():
    print(f'Bot je přihlášen jako {bot.user}')

@bot.event
async def on_message(message):
    if message.author.id == INHOUSE_BOT_ID:
        content = message.content.lower()
        # Otevření sázek
        if message.embeds and any("Red" in f.name or "Blue" in f.name for f in message.embeds[0].fields):
            await message.channel.send("💰 **Sázky otevřeny (10 min)!**", view=BettingView())
            bot.loop.create_task(ukoncit_sazky(message.channel))
        # Automatické vyhodnocení
        if "was declared winner!" in content:
            vitez = "RED" if "red team" in content else "BLUE"
            await vyhodnot_automaticky(message.channel, vitez)
            
    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
