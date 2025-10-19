from flask import Blueprint, redirect, render_template, request, session, flash, abort
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import secrets
import db



auth_bp = Blueprint('auth', __name__)


def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Kirjaudu sisään jatkaaksesi")
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def check_csrf():
    if request.method == "POST":
        if request.form.get("csrf_token") != session.get("csrf_token"):
            abort(403)

def generate_csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)
    return session["csrf_token"]



@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
        
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        
        if not username or not password1 or not password2:
            flash("Täytä kaikki kentät")
            return render_template("register.html", username=username)
            
        if len(username) < 3 or len(username) > 50:
            flash("Käyttäjätunnuksen tulee olla 3-50 merkkiä")
            return render_template("register.html", username=username)
            
        if len(password1) < 5:
            flash("Salasanan tulee olla vähintään 5 merkkiä")
            return render_template("register.html", username=username)
            
        if password1 != password2:
            flash("Salasanat eivät täsmää")
            return render_template("register.html", username=username)
            
        password_hash = generate_password_hash(password1)

        try:
            sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
            db.execute(sql, [username, password_hash])
            flash("Tunnus luotu onnistuneesti! Voit nyt kirjautua sisään.")
            return redirect("/login")
        except sqlite3.IntegrityError:
            flash("Käyttäjätunnus on jo varattu")
            return render_template("register.html", username=username)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
        
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not username or not password:
            flash("Täytä kaikki kentät")
            return render_template("login.html")

        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        results = db.query(sql, [username])
        
        if len(results) > 0:
            result = results[0]
            user_id = result["id"]
            password_hash = result["password_hash"]

            if check_password_hash(password_hash, password):
                session["user_id"] = user_id
                session["username"] = username
                session["csrf_token"] = secrets.token_hex(16)
                flash(f"Tervetuloa {username}!")
                return redirect("/")
        
        flash("Väärä tunnus tai salasana")
        return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
    if "username" in session:
        del session["username"]
    if "csrf_token" in session:
        del session["csrf_token"]
    flash("Olet kirjautunut ulos")
    return redirect("/")