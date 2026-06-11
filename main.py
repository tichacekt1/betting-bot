@bot.event
async def on_message(message):
    # Kontrola, jestli zpráva obsahuje Embed
    if message.author.id == 1001168331996409856 and message.embeds:
        embed = message.embeds[0]
        # Zkusíme vytáhnout text z popisu nebo polí embedu
        if embed.description:
            logger.info(f"Embed popis: {embed.description}")
        
        # Projdeme všechna pole (fields) v embedu, kde jsou hráči
        for field in embed.fields:
            logger.info(f"Field název: {field.name} | Hodnota: {field.value}")
            
    await bot.process_commands(message)
