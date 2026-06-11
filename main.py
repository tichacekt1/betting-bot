@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Sledujeme jen InHouse bota
    if message.author.id == 1001168331996409856:
        content = message.content.lower()

        # Pokud bot uvidí, že zápas začal (otevře sázky)
        if message.embeds and any("Red" in f.name or "Blue" in f.name for f in message.embeds[0].fields):
            await message.channel.send("💰 **Sázky otevřeny!**", view=BettingView(message.channel))
            bot.loop.create_task(ukoncit_sazky(message.channel))

        # Pokud bot uvidí, že někdo vyhlásil vítěze (vyhodnotí sázky)
        if "was declared winner!" in content:
            vitez = "RED" if "red team" in content else "BLUE"
            await vyhodnot_automaticky(message.channel, vitez)

    await bot.process_commands(message)
