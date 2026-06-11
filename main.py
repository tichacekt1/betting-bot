import discord
from discord.ext import commands

# ... (předchozí nastavení bota zůstává stejné)

class BettingView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Vsadit na RED", style=discord.ButtonStyle.red)
    async def red_bet(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"{interaction.user.name} vsadil na RED!", ephemeral=True)

    @discord.ui.button(label="Vsadit na BLUE", style=discord.ButtonStyle.primary)
    async def blue_bet(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"{interaction.user.name} vsadil na BLUE!", ephemeral=True)

@bot.event
async def on_message(message):
    if message.author.id == 1001168331996409856 and message.embeds:
        embed = message.embeds[0]
        # Hledáme, jestli embed obsahuje týmy Red/Blue
        has_teams = any("Red" in field.name or "Blue" in field.name for field in embed.fields)
        
        if has_teams:
            await message.channel.send("💰 **Sázky otevřeny!** Kdo vyhraje tento zápas?", view=BettingView())

    await bot.process_commands(message)
