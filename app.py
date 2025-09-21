import sqlite3
from flask import Flask, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import config
import db

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    sql = "SELECT * FROM recipes"
    recipes = db.query(sql)
    return render_template("index.html", recipes=recipes)

@app.route("/new_recipe")
def new_recipe():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("new_recipe.html")

@app.route("/create_recipe", methods=["POST"])
def create_recipe():
    if "user_id" not in session:
        return redirect("/login")
    
    title = request.form["title"]
    content = request.form["content"]
    user_id = session["user_id"]

    sql = "INSERT INTO recipes (title, content, user_id) VALUES (?, ?, ?)"
    db.execute(sql, [title, content, user_id])

    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
        
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        
        if password1 != password2:
            return "VIRHE: salasanat eivät ole samat"
            
        password_hash = generate_password_hash(password1)

        try:
            sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
            db.execute(sql, [username, password_hash])
        except sqlite3.IntegrityError:
            return "VIRHE: tunnus on jo varattu"

        return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
        
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        results = db.query(sql, [username])
        
        if len(results) > 0:
            result = results[0]
            user_id = result["id"]
            password_hash = result["password_hash"]

            if check_password_hash(password_hash, password):
                session["user_id"] = user_id
                session["username"] = username
                return redirect("/")
        
        return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
    if "username" in session:
        del session["username"]
    return redirect("/")

@app.route("/search")
def search():
    query = request.args.get("query", "")
    sql = "SELECT * FROM recipes WHERE title LIKE ? OR content LIKE ?"
    search_pattern = f"%{query}%"
    recipes = db.query(sql, [search_pattern, search_pattern])
    return render_template("search.html", recipes=recipes, query=query)