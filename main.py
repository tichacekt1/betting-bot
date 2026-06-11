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
    print(f"DEBUG: Bot vidí zprávu od {message.author.name}: {message.content}")
    
    if message.author == bot.user:
        return
    
    if message.author.id == INHOUSE_BOT_ID:
        embed_text = ""
        for embed in message.embeds:
            if embed.description: embed_text += embed.description.lower()
            if embed.title: embed_text += embed.title.lower()

        if "inhouse queue" in embed_text:
            try:
                await message.channel.send("💰 **Sázky otevřeny (10 min)!**", view=BettingView())
                print("Sázky úspěšně vypsány.")
            except Exception as e:
                print(f"CHYBA: {e}")
        else:
            print("DEBUG: Zpráva od InHouse bota ignorována.")

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
