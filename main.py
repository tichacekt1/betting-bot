# ID kanálu pro výsledky
RESULTS_CHANNEL_ID = 1507869769787904040

async def vyhodnot_automaticky(channel, vitez):
    if not os.path.exists('sazky.json'):
        return
    
    with open('sazky.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Najdeme kanál pro výsledky
    results_channel = channel.guild.get_channel(RESULTS_CHANNEL_ID)
    
    if not results_channel:
        await channel.send("❌ Chyba: Kanál pro výsledky nebyl nalezen!")
        return

    vitezove_text = f"🏆 **Zápas skončil! Vítězem je tým {vitez}!**\n\n**Výplatní listina:**\n"
    
    vyhry = False
    for user, saska in data.items():
        if saska['tym'] == vitez:
            vitezove_text += f"✅ {user}: vyhrál **{saska['castka']}**\n"
            vyhry = True
    
    if not vyhry:
        vitezove_text += "Nikdo nevsadil na vítězný tým."
    
    # Výsledek pošleme do specifického kanálu
    await results_channel.send(vitezove_text)
    
    # Smazání souboru
    os.remove('sazky.json')
    await channel.send("✅ Výsledky sázek byly odeslány do kanálu pro výsledky.")
