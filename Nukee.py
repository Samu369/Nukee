from flask import Flask, render_template, request, redirect
from src import discord_checks, discord_functions
import asyncio, threading, werkzeug.serving

# --- CONSTANTS ---
DEBUGGER = True

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
        if asyncio.run(discord_checks.check_token(tk)) == True:
            tk_v = "is-valid"
            if asyncio.run(discord_checks.check_server(tk, sid)) == True:
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
        discord_functions.ch_delete(token=tk, serverid=sid)
        return render_template("dashboard.html", hidden="")
    elif r == "2":
        discord_functions.ro_delete(token=tk, serverid=sid)
        return render_template("dashboard.html", hidden="")
    elif r == "3":
        discord_functions.em_delete(token=tk, serverid=sid)
        return render_template("dashboard.html", hidden="")



if __name__ == "__main__":
    def start_flask():
        global DEBUGGER
        werkzeug.serving.run_simple("localhost", 5000, app, use_reloader=False, use_debugger=DEBUGGER)
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.start()
    flask_thread.join()