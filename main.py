import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# Databáze v paměti: {user_id: {"team": "RED/BLUE"}}
current_bets = {}
betting_open = False

@bot.event
async def on_ready():
    print('--- SÁZKOVÝ BOT JE READY ---')

@bot.event
async def on_message(message):
    global betting_open
    # Detekce startu hry od InHouse bota
    if message.author.id == 1001168331996409856 and "game" in message.content.lower() and "starting" in message.content.lower():
        betting_open = True
        current_bets.clear()
        view = BettingView()
        channel = bot.get_channel(1507685027444555980)
        await channel.send("💰 **Sázky otevřeny! Kdo vyhraje?**", view=view)
    
    await bot.process_commands(message)

class BettingView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Vsadit RED", style=discord.ButtonStyle.red)
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button):
        current_bets[interaction.user.id] = "RED"
        await interaction.response.send_message("✅ Vsazeno na RED!", ephemeral=True)

    @discord.ui.button(label="Vsadit BLUE", style=discord.ButtonStyle.primary)
    async def blue(self, interaction: discord.Interaction, button: discord.ui.Button):
        current_bets[interaction.user.id] = "BLUE"
        await interaction.response.send_message("✅ Vsazeno na BLUE!", ephemeral=True)

# Příkaz pro tebe: /winner RED nebo /winner BLUE
@bot.command()
async def winner(ctx, team: str):
    global betting_open
    if ctx.channel.id != 1507869769787904040: return # Jen v kanálu výsledků
    
    betting_open = False
    team = team.upper()
    winners = [uid for uid, t in current_bets.items() if t == team]
    
    result_text = f"🏆 **Vítěz: {team}**\n\nVýherci:\n" + "\n".join([f"<@{uid}>" for uid in winners])
    await ctx.send(result_text)

bot.run("TVŮJ_TOKEN")
