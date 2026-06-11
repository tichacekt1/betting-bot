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

# Konfigurace - ID natvrdo
LOG_CHANNEL_ID = 1514649175931879455
RESULTS_CHANNEL_ID = 1507869769787904040
INHOUSE_BOT_ID = 1001168331996409856
UB_TOKEN = os.getenv("UB_API_TOKEN")
UB_GUILD_ID = "292953664492929025"

async def vyhodnot_automaticky(channel, vitez):
    if not os.path.exists('sazky.json'): return
    with open('sazky.json', 'r', encoding='utf-8') as f: data = json.load(f)
    
    results_channel = channel.guild.get_channel(RESULTS_CHANNEL_ID)
    total_bank = sum(int(s['castka']) for s in data.values())
    sum_vitezny = sum(int(s['castka']) for s in data.values() if s['tym'] == vitez)
    
    if sum_vitezny == 0:
        await results_channel.send(f"🏆 **Vítěz {vitez}, nikdo na něj nevsadil.**")
    else:
        vitezove_text = f"🏆 **Vítěz: {vitez}**\n\n**Výplatní listina:**\n"
        for user, saska in data.items():
            if saska['tym'] == vitez:
                vyhra = (int(saska['castka']) / sum_vitezny) * total_bank
                vitezove_text += f"✅ {user}: vyhrál **{round(vyhra)}**\n"
        await results_channel.send(vitezove_text)
    os.remove('sazky.json')

class BettingModal(discord.ui.Modal, title='Vsadit na zápas'):
    castka = discord.ui.TextInput(label='Kolik vsázíš?', style=discord.TextStyle.short, required=True)
    def __init__(self, tym):
        super().__init__()
        self.tym = tym
    async def on_submit(self, interaction: discord.Interaction):
        try:
            url = f"https://unbelievaboat.com/api/v1/guilds/{UB_GUILD_ID}/users/{interaction.user.id}"
            resp = requests.get(url, headers={"Authorization": UB_TOKEN}, timeout=5)
            data = resp.json() if resp.status_code == 200 else {}
            zustatek = data.get("cash", 0) + data.get("bank", 0)
        except Exception as e:
            zustatek = 0
            print(f"Chyba API: {e}")

        vsazeno = int(self.castka.value)
        if vsazeno > zustatek or vsazeno <= 0:
            await interaction.response.send_message(f"❌ Nedostatek peněz! (Máš {zustatek})", ephemeral=True)
            return

        data = {}
        if os.path.exists('sazky.json'):
            with open('sazky.json', 'r', encoding='utf-8') as f: data = json.load(f)
        data[interaction.user.name] = {"tym": self.tym, "castka": vsazeno}
        with open('sazky.json', 'w', encoding='utf-8') as f: json.dump(data, f, indent=4)
        
        await interaction.guild.get_channel(LOG_CHANNEL_ID).send(f"👤 {interaction.user.name} vsadil {vsazeno} na {self.tym}.")
        await interaction.response.send_message(f"✅ Sázka {vsazeno} přijata!", ephemeral=True)

class BettingView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=600)
    @discord.ui.button(label="Vsadit RED", style=discord.ButtonStyle.red)
    async def red(self, interaction, button): await interaction.response.send_modal(BettingModal("RED"))
    @discord.ui.button(label="Vsadit BLUE", style=discord.ButtonStyle.primary)
    async def blue(self, interaction, button): await interaction.response.send_modal(BettingModal("BLUE"))

@bot.event
async def on_message(message):
    if message.author.id == INHOUSE_BOT_ID:
        if "was declared winner!" in message.content.lower():
            vitez = "RED" if "red team" in message.content.lower() else "BLUE"
            await vyhodnot_automaticky(message.channel, vitez)
        elif message.embeds and any("Red" in f.name or "Blue" in f.name for f in message.embeds[0].fields):
            try:
                await message.channel.send("💰 **Sázky otevřeny (10 min)!**", view=BettingView())
            except discord.Forbidden:
                print("Chyba: Bot nemá oprávnění posílat zprávy do tohoto kanálu!")
    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
