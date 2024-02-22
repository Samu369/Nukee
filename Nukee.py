from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def index():
    return redirect("/nukee/login")

@app.route("/nukee/login")
def login():
    return render_template("login.html")

@app.route("/nukee/dashboard", methods=["POST"])
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)