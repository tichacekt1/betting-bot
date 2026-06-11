import discord
from discord.ext import commands
import os
import datetime
from dotenv import load_dotenv

# 1. NASTAVENÍ (vše musí být v tomto pořadí)
load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
INHOUSE_BOT_ID = 1001168331996409856

# 2. TLAČÍTKA
class BettingView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Vsadit RED", style=discord.ButtonStyle.red)
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("✅ Sázka na RED přijata!", ephemeral=True)

    @discord.ui.button(label="Vsadit BLUE", style=discord.ButtonStyle.primary)
    async def blue(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("✅ Sázka na BLUE přijata!", ephemeral=True)

# 3. UDÁLOSTI
@bot.event
async def on_ready():
    print(f'Bot {bot.user} je připraven!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # Ignoruj zprávy starší než 2 minuty
    if (datetime.datetime.now(datetime.timezone.utc) - message.created_at).total_seconds() > 120:
        return

    # Sleduj pouze InHouse bota
    if message.author.id == INHOUSE_BOT_ID:
        full_text = (message.content + " " + " ".join([e.title or "" for e in message.embeds]) + " " + " ".join([e.description or "" for e in message.embeds])).lower()
        
        # Start hry detekujeme podle těchto slov
        if "inhouse queue" in full_text and "starting" in full_text:
            # Najdi lobby kanál
            target_channel = discord.utils.get(message.guild.text_channels, name__startswith="lobby-")
            
            if target_channel:
                try:
                    await target_channel.send("💰 **Sázky otevřeny (10 min)!**", view=BettingView())
                    print(f"Sázky vypsány do: {target_channel.name}")
                except discord.Forbidden:
                    print(f"CHYBA: Nemám oprávnění psát do {target_channel.name}")
            else:
                print("DEBUG: Nenašel jsem žádné lobby.")
        else:
            print("DEBUG: Zpráva ignorována (není to start hry).")

    await bot.process_commands(message)

# 4. SPUŠTĚNÍ
bot.run(os.getenv("DISCORD_TOKEN"))
