import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

INHOUSE_BOT_ID = 1001168331996409856

class BettingModal(discord.ui.Modal, title='Vsadit na zápas'):
    castka = discord.ui.TextInput(label='Kolik vsázíš?', style=discord.TextStyle.short, required=True)
    def __init__(self, tym):
        super().__init__()
        self.tym = tym
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"✅ Sázka {self.castka.value} na {self.tym} přijata.", ephemeral=True)

class BettingView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=600)
    @discord.ui.button(label="Vsadit RED", style=discord.ButtonStyle.red)
    async def red(self, interaction, button): await interaction.response.send_modal(BettingModal("RED"))
    @discord.ui.button(label="Vsadit BLUE", style=discord.ButtonStyle.primary)
    async def blue(self, interaction, button): await interaction.response.send_modal(BettingModal("BLUE"))

@bot.event
async def on_ready():
    print(f'Bot {bot.user} je připraven!')

@bot.event
async def on_message(message):
    if message.author == bot.user: return
    
    # Detekce zprávy a automatické nastavení práv, pokud je to kanál lobby
    if message.author.id == INHOUSE_BOT_ID:
        obsah = message.content.lower()
        for embed in message.embeds:
            if embed.description: obsah += " " + embed.description.lower()
        
        if "game" in obsah and ("starting" in obsah or "found" in obsah):
            # Tady si bot vynutí práva, aby mohl do kanálu psát
            try:
                perms = message.channel.permissions_for(message.guild.me)
                if not perms.send_messages:
                    # Pokud nemůže psát, zkusí si to vynutit (vyžaduje Manage Channels)
                    await message.channel.edit(overwrites={
                        message.guild.me: discord.PermissionOverwrite(send_messages=True, read_messages=True)
                    })
                
                await message.channel.send("💰 **Sázky otevřeny (10 min)!**", view=BettingView())
                print("Sázky úspěšně vypsány.")
            except Exception as e:
                print(f"CHYBA: Bot se snažil psát, ale má blokované práva: {e}")

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
