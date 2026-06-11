import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
INHOUSE_BOT_ID = 1001168331996409856

class BettingView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Vsadit RED", style=discord.ButtonStyle.red)
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("✅ Sázka na RED přijata!", ephemeral=True)

    @discord.ui.button(label="Vsadit BLUE", style=discord.ButtonStyle.primary)
    async def blue(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("✅ Sázka na BLUE přijata!", ephemeral=True)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} je připraven!')

@bot.event
async def on_message(message):
    if message.author.id == INHOUSE_BOT_ID:
        full_text = (message.content + " " + " ".join([e.title or "" for e in message.embeds]) + " " + " ".join([e.description or "" for e in message.embeds])).lower()
        
        if "game is starting" in full_text:
            # Oprava hledání: Projdeme kanály ručně, to funguje vždy
            target_channel = None
            for channel in message.guild.text_channels:
                if "lobby" in channel.name.lower():
                    target_channel = channel
                    break
            
            if target_channel:
                try:
                    await target_channel.send("💰 **Sázky otevřeny (10 min)!**", view=BettingView())
                    print(f"Sázky úspěšně vypsány do: {target_channel.name}")
                except discord.Forbidden:
                    print(f"CHYBA: Bot nemá právo psát do {target_channel.name}!")
            else:
                print("DEBUG: Nenašel jsem žádný kanál obsahující 'lobby'.")

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
