if "game" in obsah and ("starting" in obsah or "found" in obsah):
            print("!!! DETEKCE HRY - POKOUŠÍM SE ODESLAT TLAČÍTKA !!!")
            try:
                # Zkusíme poslat zprávu do aktuálního kanálu
                await message.channel.send("💰 **Sázky otevřeny (10 min)!**", view=BettingView())
                print("Tlačítka úspěšně odeslána.")
            except discord.Forbidden:
                print("!!! CHYBA: Bot nemá oprávnění posílat zprávy v tomto kanálu !!!")
            except Exception as e:
                print(f"!!! NEOČEKÁVANÁ CHYBA: {e} !!!")
