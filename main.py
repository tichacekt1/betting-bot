import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# IDs
INHOUSE_BOT_ID = 1001168331996409856
BETTING_CHANNEL_ID = 1507685027444555980
STATS_CHANNEL_ID = 1514649175931879455
RESULTS_CHANNEL_ID = 1507869769787904040

# Jednoduché úložiště sázek v paměti
bets = {"red": 0, "blue": 0}

class BettingView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Vsadit RED", style=discord.ButtonStyle.red)
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Zde voláš příkaz pro UnbelievaBoat (pokud máš nastavenou integraci)
        # Pro začátek simulujeme přičtení do našeho počítadla
        bets["red"] += 1 
        await interaction.response.send_message("✅ Sázka na RED přijata!", ephemeral=True)
        await self.update_stats()

    @discord.ui.button(label="Vsadit BLUE", style=discord.ButtonStyle.primary)
    async def blue(self, interaction: discord.Interaction, button: discord.ui.Button):
        bets["blue"] += 1
        await interaction.response.send_message("✅ Sázka na BLUE přijata!", ephemeral=True)
        await self.update_stats()

    async def update_stats(self):
        stats_channel = bot.get_channel(STATS_CHANNEL_ID)
        if stats_channel:
            await stats_channel.send(f"📊 **Aktuální sázky:** RED: {bets['red']} | BLUE: {bets['blue']}")

@bot.event
async def on_message(message):
    if message.author.id == INHOUSE_BOT_ID and "game is starting" in message.content.lower():
        target_channel = bot.get_channel(BETTING_CHANNEL_ID)
        if target_channel:
            bets["red"] = 0 # Reset
            bets["blue"] = 0
            await target_channel.send("💰 **Sázky otevřeny!**", view=BettingView())

    # Detekce příkazu /winner pro výsledky
    if message.content.startswith("/winner"):
        results_channel = bot.get_channel(RESULTS_CHANNEL_ID)
        if results_channel:
            await results_channel.send(f"🏆 **Výsledky zápasu:** RED: {bets['red']} vs BLUE: {bets['blue']}")
    
    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
