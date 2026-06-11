@bot.event
async def on_message(message):
    # Tento řádek MUSÍ vypsat něco do terminálu pokaždé, když někdo napíše zprávu
    print(f"DEBUG: Bot vidí zprávu od {message.author.name} v kanálu {message.channel.name}: {message.content}")
    
    if message.author == bot.user:
        return
    
    if message.author.id == 1001168331996409856:
        # ... zbytek tvé logiky
