from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret123"

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT, password TEXT)")
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    if "email" in session:
        return render_template("home.html", email=session["email"])
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE email=?", (email,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[0], password):
            session["email"] = email
            return redirect("/")
        else:
            return render_template("login.html", msg="Invalid Email or Password")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (email, password) VALUES (?,?)", (email, password))
            conn.commit()
            conn.close()
            return redirect("/login")
        except:
            return render_template("signup.html", msg="Email already exists")
    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.pop("email", None)
    return redirect("/login")

if __name__ == "__main__":
    app.run()
