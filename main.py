@bot.event
async def on_message(message):
    # Logování
    if message.author != bot.user:
        logger.info(f"Zpráva od {message.author.name} (ID: {message.author.id}) v kanálu #{message.channel}: {message.content[:50]}")
    
    # KDYŽ zprávu pošle In House Queue (ID 1001168331996409856)
    if message.author.id == 1001168331996409856:
        logger.info("!!! Zachycena zpráva od In House Queue, spouštím analýzu pro sázku !!!")
        
        # Zde se spustí tvoje logika pro sázku (např. volání funkce)
        # Pokud máš funkci pro vytvoření sázky, zavolej ji tady
        # await tvoje_funkce_na_sazku(message)

    await bot.process_commands(message)
