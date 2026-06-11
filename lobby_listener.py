import discord
from discord.ext import commands
import re
import logging

logger = logging.getLogger(__name__)

class LobbyListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_bets = {}
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """Listen for Match Insights messages in lobby channels"""
        
        # Ignore bot's own messages
        if message.author.bot:
            return
        
        # Check if it's in a lobby channel
        if not message.channel.name.startswith("lobby-"):
            return
        
        # Look for Match Insights embed
        if message.embeds:
            for embed in message.embeds:
                if "Match Insights" in embed.title or "Match Insights" in str(embed.description):
                    await self.process_match_insights(message, embed)
    
    async def process_match_insights(self, message, embed):
        """Extract match data and create bet"""
        try:
            # Parse the embed to get win percentages
            content = f"{embed.title}\n{embed.description}\n"
            
            # Add field values
            for field in embed.fields:
                content += f"{field.name}: {field.value}\n"
            
            logger.info(f"Processing Match Insights:\n{content}")
            
            # Extract percentages using regex
            # Looking for patterns like "65.6%" or "34.6%"
            percentages = re.findall(r'(\d+\.?\d*)\s*%', content)
            
            if len(percentages) < 2:
                logger.warning("Could not find two percentages in Match Insights")
                return
            
            red_percentage = float(percentages[0])
            blue_percentage = float(percentages[1])
            
            logger.info(f"RED: {red_percentage}%, BLUE: {blue_percentage}%")
            
            # Calculate odds (1 / percentage)
            red_odds = 1 / (red_percentage / 100)
            blue_odds = 1 / (blue_percentage / 100)
            
            # Round to 2 decimals
            red_odds = round(red_odds, 2)
            blue_odds = round(blue_odds, 2)
            
            logger.info(f"Calculated odds - RED: {red_odds}x, BLUE: {blue_odds}x")
            
            # Extract match ID from channel name
            match_id = message.channel.name.replace("lobby-", "")
            
            # Create the bet embed
            embed_bet = discord.Embed(
                title=f"🎮 New Bet Created - Match {match_id}",
                description=f"**RED** vs **BLUE**",
                color=discord.Color.green()
            )
            embed_bet.add_field(
                name="📊 Match Insights",
                value=f"RED: {red_percentage}% ({red_odds}x odds)\nBLUE: {blue_percentage}% ({blue_odds}x odds)",
                inline=False
            )
            embed_bet.add_field(
                name="Status",
                value="🟢 Active",
                inline=False
            )
            embed_bet.add_field(
                name="Instructions",
                value="Use `/place_bet` to place your bet!",
                inline=False
            )
            
            # Store bet data
            from main import active_bets
            active_bets[match_id] = {
                "team_a": "RED",
                "team_b": "BLUE",
                "red_percentage": red_percentage,
                "blue_percentage": blue_percentage,
                "red_odds": red_odds,
                "blue_odds": blue_odds,
                "bets": {},
                "status": "active"
            }
            
            # Send the bet embed to the same channel
            await message.channel.send(embed=embed_bet)
            logger.info(f"Automatically created bet for match {match_id}")
            
        except Exception as e:
            logger.error(f"Error processing Match Insights: {e}")

async def setup(bot):
    await bot.add_cog(LobbyListener(bot))
