@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # Debug: uvidíme, co všechno bot dostává
    if message.author.id == INHOUSE_BOT_ID:
        # Zkontrolujeme text zprávy
        obsah = message.content.lower()
        
        # Zkontrolujeme i Embedy (ty barevné rámečky)
        embed_text = ""
        for embed in message.embeds:
            if embed.description:
                embed_text += embed.description.lower()
            if embed.title:
                embed_text += embed.title.lower()

        # Toto je podmínka, která hledá start hry v textu nebo v Embedu
        if "inhouse queue" in (obsah + embed_text):
            print("DEBUG: Detekován InHouse Queue start!")
            try:
                await message.channel.send("💰 **Sázky otevřeny (10 min)!**", view=BettingView())
                print("Sázky úspěšně vypsány.")
            except Exception as e:
                print(f"CHYBA: {e}")
        else:
            # Jen pro info, že to ignoruje
            pass 

    await bot.process_commands(message)
