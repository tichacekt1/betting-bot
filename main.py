import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

INHOUSE_BOT_ID = 1001168331996409856
TARGET_CHANNEL_ID = 1507685027444555980

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
            # Bot nyní cílí PŘÍMO na tvoje ID kanálu
            target_channel = bot.get_channel(TARGET_CHANNEL_ID)
            
            if target_channel:
                try:
                    await target_channel.send("💰 **Sázky otevřeny (10 min)!**", view=BettingView())
                    print(f"Sázky úspěšně vypsány do kanálu: {target_channel.name}")
                except discord.Forbidden:
                    print(f"CHYBA: Bot nemá právo psát do kanálu s ID {TARGET_CHANNEL_ID}!")
            else:
                print(f"CHYBA: Bot nevidí kanál s ID {TARGET_CHANNEL_ID}. Zkontroluj, jestli tam bot je!")

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
