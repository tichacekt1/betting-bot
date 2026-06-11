@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Debug: uvidíme, jestli zpráva obsahuje embedy
    has_embeds = len(message.embeds) > 0
    print(f"DEBUG: Autor: {message.author.name} | Obsah: '{message.content}' | Embedů: {has_embeds}")

    if message.author.id == INHOUSE_BOT_ID:
        # Zkontrolujeme, jestli zpráva nebo její embedy obsahují klíčová slova
        text_to_check = message.content.lower()
        if has_embeds:
            for embed in message.embeds:
                if embed.description:
                    text_to_check += " " + embed.description.lower()
                if embed.title:
                    text_to_check += " " + embed.title.lower()

        # Pokud se v textu nebo embedu objeví "game" a "ready" nebo "found"
        if "game" in text_to_check and ("ready" in text_to_check or "found" in text_to_check):
            print("!!! DETEKCE HRY V EMBEDU - ODESÍLÁM TLAČÍTKA !!!")
            try:
                await message.channel.send("💰 **Sázky otevřeny (10 min)!**", view=BettingView())
            except Exception as e:
                print(f"CHYBA: {e}")

    await bot.process_commands(message)
