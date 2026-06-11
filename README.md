# 🎮 Betting Bot

Discord bot for creating and managing bets on InHouse Queue matches with UnbelivaBOAT integration.

## Features

- ✅ Create bets for InHouse matches
- ✅ Place bets on teams
- ✅ Track active bets
- ✅ End matches and announce winners
- ✅ Integration with UnbelivaBOAT (coming soon)

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/tichacekt1/betting-bot.git
cd betting-bot
```

### 2. Create virtual environment
```bash
python -m venv venv
```

**On Windows:**
```bash
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup environment variables
Copy `.env.example` to `.env` and fill in your values:
```bash
cp .env.example .env
```

Edit `.env` with:
- `DISCORD_TOKEN` - Your bot token from Discord Developer Portal
- `GUILD_ID` - Your Discord server ID (optional for slash commands)

### 5. Run the bot
```bash
python main.py
```

## Commands

### `/create_bet`
Create a new bet for a match
```
/create_bet match_id:1 team_a:Team1 team_b:Team2
```

### `/place_bet`
Place a bet on a team
```
/place_bet match_id:1 team:A amount:100
```

### `/end_match`
End a match and announce winner
```
/end_match match_id:1 winner:A
```

### `/bet_status`
Check all active bets
```
/bet_status
```

## TODO

- [ ] InHouse Queue bot integration (automatic match detection)
- [ ] UnbelivaBOAT API integration (automatic coin distribution)
- [ ] Database for persistent bet storage
- [ ] Bet history and statistics
- [ ] Admin commands

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT