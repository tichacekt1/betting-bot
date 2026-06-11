import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Store active bets
active_bets = {}

@bot.event
async def on_ready():
    logger.info(f"Bot is ready! Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        logger.info(f"Synced {len(synced)} command(s)")
    except Exception as e:
        logger.error(f"Failed to sync commands: {e}")

@bot.tree.command(name="create_bet", description="Create a new bet for a match")
@discord.app_commands.describe(
    match_id="ID of the InHouse match",
    team_a="Team A name",
    team_b="Team B name"
)
async def create_bet(interaction: discord.Interaction, match_id: str, team_a: str, team_b: str):
    """Create a new betting match"""
    try:
        if match_id in active_bets:
            await interaction.response.send_message(f"❌ Bet for match {match_id} already exists!", ephemeral=True)
            return
        
        active_bets[match_id] = {
            "team_a": team_a,
            "team_b": team_b,
            "bets": {},
            "status": "active"
        }
        
        embed = discord.Embed(
            title=f"🎮 New Bet Created - Match {match_id}",
            description=f"**{team_a}** vs **{team_b}**",
            color=discord.Color.green()
        )
        embed.add_field(name="Status", value="🟢 Active", inline=False)
        embed.add_field(name="Instructions", value="Use `/place_bet` to place your bet!", inline=False)
        
        await interaction.response.send_message(embed=embed)
        logger.info(f"Created bet for match {match_id}")
        
    except Exception as e:
        logger.error(f"Error creating bet: {e}")
        await interaction.response.send_message(f"❌ Error: {str(e)}", ephemeral=True)

@bot.tree.command(name="place_bet", description="Place a bet on a match")
@discord.app_commands.describe(
    match_id="ID of the match to bet on",
    team="Team to bet on (A or B)",
    amount="Amount to bet"
)
async def place_bet(interaction: discord.Interaction, match_id: str, team: str, amount: int):
    """Place a bet on a specific team"""
    try:
        if match_id not in active_bets:
            await interaction.response.send_message(f"❌ No active bet for match {match_id}", ephemeral=True)
            return
        
        team = team.upper()
        if team not in ["A", "B"]:
            await interaction.response.send_message("❌ Team must be 'A' or 'B'", ephemeral=True)
            return
        
        if amount <= 0:
            await interaction.response.send_message("❌ Bet amount must be positive", ephemeral=True)
            return
        
        user_id = interaction.user.id
        if user_id not in active_bets[match_id]["bets"]:
            active_bets[match_id]["bets"][user_id] = {}
        
        active_bets[match_id]["bets"][user_id][team] = amount
        
        team_name = active_bets[match_id][f"team_{team.lower()}"]
        embed = discord.Embed(
            title="✅ Bet Placed!",
            description=f"You bet **{amount} coins** on **{team_name}**",
            color=discord.Color.green()
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        logger.info(f"User {interaction.user.name} placed bet: {amount} on team {team}")
        
    except Exception as e:
        logger.error(f"Error placing bet: {e}")
        await interaction.response.send_message(f"❌ Error: {str(e)}", ephemeral=True)

@bot.tree.command(name="end_match", description="End a match and distribute winnings")
@discord.app_commands.describe(
    match_id="ID of the match",
    winner="Winning team (A or B)"
)
async def end_match(interaction: discord.Interaction, match_id: str, winner: str):
    """End a match and announce winner"""
    try:
        if match_id not in active_bets:
            await interaction.response.send_message(f"❌ No active bet for match {match_id}", ephemeral=True)
            return
        
        winner = winner.upper()
        if winner not in ["A", "B"]:
            await interaction.response.send_message("❌ Winner must be 'A' or 'B'", ephemeral=True)
            return
        
        bet_data = active_bets[match_id]
        winning_team = bet_data[f"team_{winner.lower()}"]
        
        # Calculate winnings
        winners_list = []
        for user_id, bets in bet_data["bets"].items():
            if winner in bets:
                winners_list.append({
                    "user_id": user_id,
                    "winnings": bets[winner]  # Zde byla opravena chyba (smazáno * 2)
                })
        
        embed = discord.Embed(
            title=f"🏆 Match {match_id} - Final Result",
            description=f"**{winning_team}** wins!",
            color=discord.Color.gold()
        )
        
        if winners_list:
            winners_text = "\n".join([f"<@{w['user_id']}> wins {w['winnings']} coins" for w in winners_list])
            embed.add_field(name="Winners", value=winners_text, inline=False)
        else:
            embed.add_field(name="Winners", value="No winners for this match", inline=False)
        
        # Mark match as completed
        active_bets[match_id]["status"] = "completed"
        
        await interaction.response.send_message(embed=embed)
        logger.info(f"Match {match_id} ended. Winner: {winning_team}")
        
        # TODO: Here we would integrate with UnbelivaBOAT API to add coins to winners
        
    except Exception as e:
        logger.error(f"Error ending match: {e}")
        await interaction.response.send_message(f"❌ Error: {str(e)}", ephemeral=True)

@bot.tree.command(name="bet_status", description="Check status of active bets")
async def bet_status(interaction: discord.Interaction):
    """Check all active bets"""
    try:
        if not active_bets:
            await interaction.response.send_message("❌ No active bets", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="📊 Active Bets",
            color=discord.Color.blue()
        )
        
        for match_id, data in active_bets.items():
            if data["status"] == "active":
                bet_count = len(data["bets"])
                embed.add_field(
                    name=f"Match {match_id}",
                    value=f"{data['team_a']} vs {data['team_b']}\nBets placed: {bet_count}",
                    inline=False
                )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
    except Exception as e:
        logger.error(f"Error checking bet status: {e}")
        await interaction.response.send_message(f"❌ Error: {str(e)}", ephemeral=True)

# Run the bot
if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        logger.error("DISCORD_TOKEN not found in .env file")
        exit(1)
    
    bot.run(token)
