@bot.event
async def on_message(message):
    # Logování všeho, co bot vidí
    logger.info(f"Zpráva od {message.author} v kanálu #{message.channel}: {message.content[:50]}")
    
    # Debug: Vypiš ID autora, abychom zjistili, jestli se shoduje
    if message.author != bot.user:
        logger.info(f"Autor ID: {message.author.id}")

    await bot.process_commands(message)
