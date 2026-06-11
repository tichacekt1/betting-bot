import discord
from discord.ext import commands
import os
import json
import asyncio
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ID kanálu, kam se budou logovat sázky
LOG_CHANNEL_ID = 1514649175931879455

async def ukoncit_sazky(channel):
    await asyncio.sleep(600)  # 10 minut
    await channel.send("🚫 **Sázky uzavřeny!** Čeká se na vyhlášení vítěze.")

class BettingModal(discord.ui.Modal, title='Vsadit na zápas'):
    castka = discord.ui.TextInput(label='Kolik chceš vsadit?', style=discord.TextStyle.short, required=True)

    def __init__(self, tym, channel):
        super().__init__()
        self.tym = tym
        self.channel = channel

    async def on_submit(self, interaction: discord.Interaction):
        # Načtení/Vytvoření souboru
        data = {}
        if os.path.exists('sazky.json'):
            with open('sazky.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        
        # Přidání sázky
        data[interaction.user.name] = {"tym": self.tym, "castka": self.castka.value}
        
        with open('sazky.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        
        # Odeslání do logovacího kanálu
        log_channel = interaction.guild.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(f"👤 **{interaction.user.name}** vsadil **{self.castka.value}** na tým **{self.tym}**.")
            
        await interaction.response.send_message(f"✅ Sázka {self.castka.value} na {self.tym} byla uložena!", ephemeral=True)

class BettingView(discord.ui.View):
    def __init__(self, channel):
        super().__init__(timeout=600)
        self.channel = channel

    @discord.ui.button(label="Vsadit na RED", style=discord.ButtonStyle.red)
    async def red_bet(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(BettingModal("RED", self.channel))

    @discord.ui.button(label="Vsadit na BLUE", style=discord.ButtonStyle.primary)
    async def blue_bet(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(BettingModal("BLUE", self.channel))

@bot.event
async def on_message(message):
    if message.author.id == 1001168331996409856 and message.embeds:
        if any("Red" in f.name or "Blue" in f.name for f in message.embeds[0].fields):
            await message.channel.send("💰 **Sázky otevřeny (10 min)!**", view=BettingView(message.channel))
            bot.loop.create_task(ukoncit_sazky(message.channel))
    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
