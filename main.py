@bot.event
async def on_message(message):
    # Tohle vypíše do konzole ÚPLNĚ KAŽDOU zprávu, kterou bot kdekoli uvidí
    print(f"DEBUG: Kanál: {message.channel.name} | Autor: {message.author.name} | Obsah: {message.content[:50]}")
    
    # Ignoruj zprávy od sebe
    if message.author == bot.user:
        return

    # Podmínka: Pokud zpráva obsahuje "game" a "starting" (nebo "lobby")
    content = message.content.lower()
    if "game" in content and ("starting" in content or "found" in content):
        print("!!! DETEKCE HRY - ODESÍLÁM TLAČÍTKA !!!")
        try:
            await message.channel.send("💰 **Sázky otevřeny (10 min)!**", view=BettingView())
        except Exception as e:
            print(f"CHYBA PŘI ODESÍLÁNÍ: {e}")

    await bot.process_commands(message)
