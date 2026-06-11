import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

# 1. Nastavení
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

INHOUSE_BOT_ID = 1001168331996409856

# 2. Definice tlačítek
class BettingView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Vsadit RED", style=discord.ButtonStyle.red)
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("✅ Sázka na RED přijata!", ephemeral=True)

    @discord.ui.button(label="Vsadit BLUE", style=discord.ButtonStyle.primary)
    async def blue(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("✅ Sázka na BLUE přijata!", ephemeral=True)

# 3. Události
@bot.event
async def on_ready():
    print(f'Bot {bot.user} je připraven!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.author.id == INHOUSE_BOT_ID:
        # Sestavíme text ze zprávy i z embedů
        full_text = message.content.lower()
        for embed in message.embeds:
            if embed.title: full_text += embed.title.lower()
            if embed.description: full_text += embed.description.lower()
        
        # Hledáme klíčové slovo
        if "inhouse queue" in full_text or "game" in full_text:
            try:
                await message.channel.send("💰 **Sázky otevřeny (10 min)!**", view=BettingView())
                print("Sázky úspěšně vypsány.")
            except Exception as e:
                print(f"CHYBA při odesílání: {e}")
        else:
            print(f"DEBUG: Zpráva ignorována. Obsah: {full_text[:50]}...")

    await bot.process_commands(message)

# 4. Spuštění
bot.run(os.getenv("DISCORD_TOKEN"))
