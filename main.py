import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging
import aiohttp

# Načtení proměnných prostředí
load_dotenv()

# Nastavení logování
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Nastavení Discord bota
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Fixní konfigurace podle tvého serveru
GUILD_ID = 709482555300118580         # ID tvého serveru
INHOUSE_BOT_ID = 1001168331996409856   # ID tvého InHouse Queue bota

# Paměť pro aktivní sázky
active_bets = {}

# Pomocná funkce pro UnbelivaBOAT API
async def modify_user_balance(user_id: int, amount: int, reason: str):
    unb_token = os.getenv("UNB_TOKEN")
    if not unb_token:
        logger.error("UNB_TOKEN chybí v .env souboru!")
        return False
    
    url = f"https://unbelivaboat.com/api/v1/guilds/{GUILD_ID}/users/{user_id}"
    headers = {"Authorization": unb_token, "Content-Type": "application/json"}
    data = {"cash": amount, "reason": reason}
    
    async with aiohttp.ClientSession() as session:
        async with session.patch(url, headers=headers, json=data) as response:
            if response.status == 200:
                return True
            else:
                resp_text = await response.text()
                logger.error(f"UnbelivaBOAT API error ({response.status}): {resp_text}")
                return False

@bot.event
async def on_ready():
    logger.info(f"Sázkový bot je připraven! Přihlášen jako {bot.user}")
    try:
        synced = await bot.tree.sync()
        logger.info(f"Synchronizováno {len(synced)} příkazů.")
    except Exception as e:
        logger.error(f"Chyba při synchronizaci příkazů: {e}")

# Sledování zpráv – zachycení zprávy od InHouse bota a vyhodnocování výher
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Pokud přijde zpráva do lobby kanálu
    if isinstance(message.channel, discord.TextChannel) and message.channel.name.startswith("lobby-"):
        
        # 1. AUTOMATICKÉ OTEVŘENÍ SÁZEK (Zprávu poslal InHouse bot a sázky ještě neběžely)
        if message.author.id == INHOUSE_BOT_ID:
            match_id = message.channel.name.replace("lobby-", "")
            
            if match_id not in active_bets:
                active_bets[match_id] = {
                    "team_a": "BLUE",
                    "team_b": "RED",
                    "bets": {},
                    "status": "active",
                    "channel_id": message.channel.id
                }
                
                logger.info(f"InHouse bot poslal zprávu v {message.channel.name}. Zakládám sázky pro zápas: {match_id}")
                
                embed = discord.Embed(
                    title=f"🎮 Sázky automaticky otevřeny! • Zápas {match_id}",
                    description="🔵 **BLUE** vs 🔴 **RED**\n\nVsaďte si na vítěze tohoto zápasu pomocí příkazu `/place_bet`!",
                    color=discord.Color.blue()
                )
                embed.add_field(name="Sázkový systém", value="Jedná se o pool sázky (totalizátor). Celkový bank poražených se na konci spravedlivě rozdělí mezi výherce podle výše jejich sázky.", inline=False)
                embed.add_field(name="Stav sázek", value="🟢 Sázky jsou OTEVŘENY", inline=False)
                
                try:
                    await message.channel.send(embed=embed)
                    logger.info(f"Sázková tabulka úspěšně odeslána do {message.channel.name}")
                except Exception as e:
                    logger.error(f"Nepodařilo se poslat sázkovou tabulku: {e}")

        # 2. VYHODNOCENÍ ZÁPASU (Hráč poslal příkaz k ukončení)
        content_lower = message.content.lower()
        if "!win" in content_lower or "/win" in content_lower or "/winner" in content_lower:
            current_match_id = None
            for m_id, data in active_bets.items():
                if data["channel_id"] == message.channel.id and data["status"] == "active":
                    current_match_id = m_id
                    break
            
            if current_match_id:
                winner = None
                if "blue" in content_lower:
                    winner = "A"
                elif "red" in content_lower:
                    winner = "B"
                
                if winner:
                    await process_match_payout(message.channel, current_match_id, winner)

    await bot.process_commands(message)

# Výpočet podílů z banku a odeslání peněz
async def process_match_payout(channel, match_id: str, winner: str):
    bet_data = active_bets[match_id]
    bet_data["status"] = "completed"
    
    winning_team_name = bet_data["team_a"] if winner == "A" else bet_data["team_b"]
    total_pool = 0
    total_winning_bets = 0
    
    for user_id, user_bets in bet_data["bets"].items():
        total_pool += sum(user_bets.values())
        if winner in user_bets:
            total_winning_bets += user_bets[winner]
            
    embed = discord.Embed(
        title=f"🏆 Zápas {match_id} ukončen!",
        description=f"Tým **{winning_team_name}** vyhrál zápas!",
        color=discord.Color.gold()
    )
    embed.add_field(name="📊 Celkový bank na stole", value=f"**{total_pool} coins**", inline=True)
    
    if total_winning_bets > 0:
        odds = round(total_pool / total_winning_bets, 2)
        embed.add_field(name="📈 Výsledný Kurz", value=f"**x{odds}**", inline=True)
        
        winners_text = []
        for user_id, user_bets in bet_data["bets"].items():
            if winner in user_bets:
                user_share = user_bets[winner] / total_winning_bets
                winnings = int(total_pool * user_share)
                profit = winnings - user_bets[winner]
                
                success = await modify_user_balance(user_id, winnings, f"Vyhraná sázka - Zápas {match_id}")
                
                if success:
                    winners_text.append(f"<@{user_id}> vyhrává **{winnings} coins** (Čistý zisk: +{profit})")
                else:
                    winners_text.append(f"<@{user_id}> vyhrál **{winnings} coins**, ale nepodařilo se kontaktovat banku.")
        
        embed.add_field(name="💰 Výherci sázek", value="\n".join(winners_text), inline=False)
    else:
        embed.add_field(name="💰 Výherci sázek", value="Nikdo nevsadil na vítězný tým. Bank propadá serveru.", inline=False)
        
    await channel.send(embed=embed)

# Lomítkový příkaz pro podání sázky
@bot.tree.command(name="place_bet", description="Vsadit si na zápas v tomto lobby")
@discord.app_commands.describe(team="Tým (A = BLUE, B = RED)", amount="Částka sázky")
async def place_bet(interaction: discord.Interaction, team: str, amount: int):
    try:
        match_id = None
        for m_id, data in active_bets.items():
            if data["channel_id"] == interaction.channel_id and data["status"] == "active":
                match_id = m_id
                break
                
        if not match_id:
            await interaction.response.send_message("❌ V tomto kanálu momentálně neběží žádná aktivní sázka.", ephemeral=True)
            return
            
        team = team.upper()
        if team not in ["A", "B"]:
            await interaction.response.send_message("❌ Neplatný tým! Zadej 'A' pro BLUE nebo 'B' pro RED.", ephemeral=True)
            return
            
        if amount <= 0:
            await interaction.response.send_message("❌ Částka sázky musí být vyšší než 0!", ephemeral=True)
            return
            
        user_id = interaction.user.id
        team_name = active_bets[match_id]["team_a"] if team == "A" else active_bets[match_id]["team_b"]
        
        success = await modify_user_balance(user_id, -amount, f"Sázka na zápas {match_id}")
        
        if not success:
            await interaction.response.send_message("❌ Sázku nebylo možné provést. Buď nemáš dostatek coinů v UnbelivaBOAT, nebo bot nemá práva.", ephemeral=True)
            return
            
        if user_id not in active_bets[match_id]["bets"]:
            active_bets[match_id]["bets"][user_id] = {}
            
        active_bets[match_id]["bets"][user_id][team] = active_bets[match_id]["bets"][user_id].get(team, 0) + amount
        
        await interaction.response.send_message(f"✅ Úspěšně vsazeno **{amount} coins** na tým **{team_name}**!", ephemeral=True)
        
    except Exception as e:
        logger.error(f"Chyba při podání sázky: {e}")
        await interaction.response.send_message("❌ Nastala interní chyba při zpracování sázky.", ephemeral=True)

if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        logger.error("DISCORD_TOKEN nebyl nalezen v .env souboru!")
        exit(1)
    bot.run(token)
