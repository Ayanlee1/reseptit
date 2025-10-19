from flask import Flask, redirect, render_template, request, session, flash
import config
import db
from auth import auth_bp, login_required, check_csrf, generate_csrf_token
from recipes import recipes_bp
from reviews import reviews_bp
from users import users_bp
from categories import categories_bp

app = Flask(__name__)
app.secret_key = config.secret_key

app.register_blueprint(auth_bp)
app.register_blueprint(recipes_bp)
app.register_blueprint(reviews_bp)
app.register_blueprint(users_bp)
app.register_blueprint(categories_bp)


@app.route("/")
def index():
    sql = """SELECT r.id, r.title, r.content, u.username, u.id as user_id 
             FROM recipes r, users u 
             WHERE r.user_id = u.id 
             ORDER BY r.id DESC"""
    recipes = db.query(sql)
    return render_template("index.html", recipes=recipes)


@app.route("/search")
def search():
    query = request.args.get("query", "")
    if query:
        sql = """SELECT r.id, r.title, r.content, u.username 
                 FROM recipes r, users u 
                 WHERE r.user_id = u.id 
                 AND (r.title LIKE ? OR r.content LIKE ?) 
                 ORDER BY r.id DESC"""
        search_pattern = f"%{query}%"
        recipes = db.query(sql, [search_pattern, search_pattern])
    else:
        recipes = []
    
    return render_template("search.html", recipes=recipes, query=query)


@app.context_processor
def inject_csrf_token():
    return dict(csrf_token=generate_csrf_token())



