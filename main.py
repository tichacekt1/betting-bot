import discord
from discord.ext import commands
import os
import datetime
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
    if message.author == bot.user:
        return
    
    # Sledujeme pouze InHouse bota
    if message.author.id == INHOUSE_BOT_ID:
        # Vytiskneme úplně všechno, co bot poslal, do terminálu, abychom to viděli
        full_content = message.content.lower()
        embed_info = ""
        for embed in message.embeds:
            embed_info += f" | Title: {embed.title} | Desc: {embed.description}"
        
        print(f"DEBUG: InHouse bot poslal: {full_content} {embed_info.lower()}")

        # Tady je uvolněná podmínka - hledáme jakoukoli zmínku o hře
        if "game" in (full_content + embed_info.lower()):
            target_channel = discord.utils.get(message.guild.text_channels, name__startswith="lobby-")
            if target_channel:
                await target_channel.send("💰 **Sázky otevřeny (10 min)!**", view=BettingView())
                print(f"Sázky úspěšně vypsány do: {target_channel.name}")
            else:
                print("DEBUG: Nenašel jsem kanál začínající 'lobby-'.")
        else:
            print("DEBUG: Zpráva ignorována (neobsahuje slovo 'game').")

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
