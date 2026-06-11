@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # DIAGNOSTIKA: Vypíše do terminálu každou zprávu, kterou bot zachytí
    print(f"DEBUG: Zachycena zpráva od {message.author.name}: {message.content}")
    
    if message.author.id == 1001168331996409856: # ID InHouse bota
        obsah = message.content.lower()
        # Přidej diagnostiku pro kontrolu, co bot vyhodnocuje
        print(f"DEBUG: Kontrola obsahu: {obsah}")
        
        if "game" in obsah and ("starting" in obsah or "found" in obsah):
            print("DEBUG: Podmínka pro sázky splněna!")
            try:
                await message.channel.send("💰 **Sázky otevřeny (10 min)!**", view=BettingView())
                print("Sázky úspěšně vypsány.")
            except discord.Forbidden:
                print("CHYBA: Bot stále nemá právo psát do tohoto kanálu!")
    
    await bot.process_commands(message)
