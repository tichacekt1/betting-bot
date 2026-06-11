import datetime # Přidej import datetime na začátek souboru

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # Ignoruj zprávy starší než 2 minuty (aby nepsal na staré konce her)
    if (datetime.datetime.now(datetime.timezone.utc) - message.created_at).total_seconds() > 120:
        return

    if message.author.id == INHOUSE_BOT_ID:
        full_text = message.content.lower()
        for embed in message.embeds:
            if embed.title: full_text += embed.title.lower()
            if embed.description: full_text += embed.description.lower()
        
        # Reaguj jen na "inhouse queue" A ZÁROVEŇ to musí být "starting"
        if "inhouse queue" in full_text and "starting" in full_text:
            target_channel = None
            # Hledáme kanál, který patří k aktuální hře
            for channel in message.guild.text_channels:
                if channel.name.startswith("lobby-"):
                    target_channel = channel
                    break
            
            if target_channel:
                await target_channel.send("💰 **Sázky otevřeny (10 min)!**", view=BettingView())
                print(f"Sázky vypsány do: {target_channel.name}")
