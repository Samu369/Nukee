from flask import Flask, render_template, request, redirect

app = Flask(__name__)



@app.route("/")
def index():
    return redirect("/nukee/login")

@app.route("/nukee/login")
def login():
    global tk_v
    return render_template("login.html", tk_v=tk_v)

@app.route("/nukee/dashboard", methods=["POST"])
def dashboard():
    if request.form["token"] == "":
        global tk_v
        tk_v = "is-invalid"
        return redirect("/nukee/login")
    return render_template("dashboard.html")

if __name__ == "__main__":
    tk_v = ""
    app.run(debug=True)