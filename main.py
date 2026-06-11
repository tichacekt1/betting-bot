import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=infents) # Opraven překlep v intents

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
    
    # Debug: uvidíme, co všechno bot dostává
    if message.author.id == INHOUSE_BOT_ID:
        print(f"DEBUG: Bot vidí zprávu od In House Queue.")
        
        # Sestavíme veškerý text, který bot poslal
        obsah = message.content.lower()
        embed_data = ""
        for embed in message.embeds:
            if embed.title: embed_data += embed.title.lower()
            if embed.description: embed_data += embed.description.lower()
            for field in embed.fields:
                embed_data += field.value.lower()
        
        celkovy_text = obsah + embed_data
        
        # Hledáme klíčové ukazatele startu hry
        if "inhouse queue" in celkovy_text or "game is starting" in celkovy_text or "game was found" in celkovy_text:
            print("DEBUG: Podmínka pro start hry splněna!")
            try:
                await message.channel.send("💰 **Sázky otevřeny (10 min)!**", view=BettingView())
                print("Sázky úspěšně vypsány.")
            except Exception as e:
                print(f"CHYBA při odesílání: {e}")
        else:
            print(f"DEBUG: Zpráva ignorována. Obsah: {celkovy_text[:50]}...")
    
    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
