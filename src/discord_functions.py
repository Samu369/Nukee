import discord

# --- Discord Functions ---
def ch_delete(token: str, serverid: int): # Elimina tutti i canali
    try:
        intents = discord.Intents.default()
        intents.all()
        client = discord.Client(intents=intents)
        @client.event
        async def on_ready():
            print('--- ELIMINAZIONE CANALI ---')
            server = client.get_guild(serverid)
            if server:
                canali = server.channels
                for c in canali:
                    try:
                        await c.delete()
                        print(f'Canale eliminato: {c.name} | {c.id}')
                    except Exception as e:
                        print(f'[{e}] Impossibile eliminare: {c.name} | {c.id}')
                        continue
                print("--- OPERAZIONE TERMINATA ---\n")
            else:
                print("IMPOSSIBILE TROVARE IL SERVER\n")
            await client.close()        
        client.run(token)
    except Exception as e:
        print(f"ERRORE: {e}\n")

def ro_delete(token: str, serverid: int): # Elimina tutti i ruoli
    try:
        intents = discord.Intents.default()
        intents.all()
        client = discord.Client(intents=intents)
        @client.event
        async def on_ready():
            print('--- ELIMINAZIONE RUOLI ---')
            server = client.get_guild(serverid)
            if server:
                ruoli = server.roles
                for r in ruoli:
                    if r.name != '@everyone':
                        try:
                            await r.delete()
                            print(f'Ruolo eliminato: {r.name} | {r.id}')
                        except Exception as e:
                            print(f'[{e}] Impossibile eliminare il ruolo: {r.name} | {r.id}')
                            continue
                print("--- OPERAZIONE TERMINATA ---\n")
            else:
                print("IMPOSSIBILE TROVARE IL SERVER\n")
            await client.close()
        client.run(token)
    except Exception as e:
        print(f"ERRORE: {e}\n")

def em_delete(token: str, serverid: int): # Elimina tutte le emoji
    try:
        intents = discord.Intents.default()
        intents.all()
        client = discord.Client(intents=intents)
        @client.event
        async def on_ready():
            print('--- ELIMINAZIONE RUOLI ---')
            server = client.get_guild(serverid)
            if server:
                emoji = server.emojis
                for em in emoji:
                    try:
                        await em.delete()
                        print(f'Emoji eliminata: {em.name} | {em.id}')
                    except Exception as e:
                        print(f'[{e}] Impossibile eliminare: {em.name} | {em.id}')
                        continue
                print("--- OPERAZIONE TERMINATA ---\n")
            else:
                print("IMPOSSIBILE TROVARE IL SERVER\n")
            await client.close()        
        client.run(token)
    except Exception as e:
        print(f"ERRORE: {e}\n")
