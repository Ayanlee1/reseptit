import sqlite3
from flask import Flask, redirect, render_template, request, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
import config
import db

app = Flask(__name__)
app.secret_key = config.secret_key


@app.route("/")
def index():
    sql = "SELECT r.id, r.title, r.content, u.username FROM recipes r, users u WHERE r.user_id = u.id ORDER BY r.id DESC"
    recipes = db.query(sql)
    return render_template("index.html", recipes=recipes)


@app.route("/new_recipe")
def new_recipe():
    if "user_id" not in session:
        return redirect("/login")
    
    categories_sql = "SELECT id, name FROM categories ORDER BY name"
    categories = db.query(categories_sql)
    return render_template("new_recipe.html", categories=categories)


@app.route("/create_recipe", methods=["POST"])
def create_recipe():
    if "user_id" not in session:
        return redirect("/login")
    
    title = request.form["title"]
    content = request.form["content"]
    user_id = session["user_id"]
    
    if not title or not content:
        flash("Otsikko ja sisältö eivät voi olla tyhjiä")
        return redirect("/new_recipe")

    sql = "INSERT INTO recipes (title, content, user_id) VALUES (?, ?, ?)"
    db.execute(sql, [title, content, user_id])
    
    recipe_id = db.last_insert_id()
    categories = request.form.getlist("categories")
    
    for category_id in categories:
        category_sql = "INSERT INTO recipe_categories (recipe_id, category_id) VALUES (?, ?)"
        db.execute(category_sql, [recipe_id, category_id])
    
    flash("Resepti lisätty onnistuneesti")
    return redirect("/")


@app.route("/edit_recipe/<int:recipe_id>")
def edit_recipe(recipe_id):
    if "user_id" not in session:
        return redirect("/login")
    
    sql = "SELECT * FROM recipes WHERE id = ?"
    result = db.query(sql, [recipe_id])
    
    if not result:
        flash("Reseptiä ei löytynyt")
        return redirect("/")
    
    recipe = result[0]
    
    if recipe["user_id"] != session["user_id"]:
        flash("Voit muokata vain omia reseptejäsi")
        return redirect("/")
    
    categories_sql = "SELECT id, name FROM categories ORDER BY name"
    categories = db.query(categories_sql)
    
    current_sql = "SELECT category_id FROM recipe_categories WHERE recipe_id = ?"
    current_categories = db.query(current_sql, [recipe_id])
    current_ids = [c["category_id"] for c in current_categories]
    
    return render_template("edit_recipe.html", recipe=recipe, categories=categories, current_ids=current_ids)


@app.route("/update_recipe/<int:recipe_id>", methods=["POST"])
def update_recipe(recipe_id):
    if "user_id" not in session:
        return redirect("/login")
    
    check_sql = "SELECT user_id FROM recipes WHERE id = ?"
    result = db.query(check_sql, [recipe_id])
    
    if not result or result[0]["user_id"] != session["user_id"]:
        flash("Voit muokata vain omia reseptejäsi")
        return redirect("/")
    
    title = request.form["title"]
    content = request.form["content"]
    
    if not title or not content:
        flash("Otsikko ja sisältö eivät voi olla tyhjiä")
        return redirect(f"/edit_recipe/{recipe_id}")
    
    update_sql = "UPDATE recipes SET title = ?, content = ? WHERE id = ?"
    db.execute(update_sql, [title, content, recipe_id])
    
    delete_sql = "DELETE FROM recipe_categories WHERE recipe_id = ?"
    db.execute(delete_sql, [recipe_id])
    
    categories = request.form.getlist("categories")
    for category_id in categories:
        category_sql = "INSERT INTO recipe_categories (recipe_id, category_id) VALUES (?, ?)"
        db.execute(category_sql, [recipe_id, category_id])
    
    flash("Reseptiä muokattu onnistuneesti")
    return redirect("/")


@app.route("/delete_recipe/<int:recipe_id>", methods=["POST"])
def delete_recipe(recipe_id):
    if "user_id" not in session:
        return redirect("/login")
    
    check_sql = "SELECT user_id FROM recipes WHERE id = ?"
    result = db.query(check_sql, [recipe_id])
    
    if not result or result[0]["user_id"] != session["user_id"]:
        flash("Voit poistaa vain omia reseptejäsi")
        return redirect("/")
    
    delete_sql = "DELETE FROM recipes WHERE id = ?"
    db.execute(delete_sql, [recipe_id])
    
    flash("Resepti poistettu onnistuneesti")
    return redirect("/")


@app.route("/recipe/<int:recipe_id>")
def recipe_page(recipe_id):
    sql = "SELECT r.id, r.title, r.content, u.username, u.id as user_id FROM recipes r, users u WHERE r.id = ? AND r.user_id = u.id"
    result = db.query(sql, [recipe_id])
    
    if not result:
        flash("Reseptiä ei löytynyt")
        return redirect("/")
    
    recipe = result[0]
    
    categories_sql = "SELECT c.name FROM categories c, recipe_categories rc WHERE rc.recipe_id = ? AND rc.category_id = c.id"
    categories = db.query(categories_sql, [recipe_id])
    
    reviews_sql = "SELECT r.comment, r.rating, u.username FROM reviews r, users u WHERE r.recipe_id = ? AND r.user_id = u.id ORDER BY r.id DESC"
    reviews = db.query(reviews_sql, [recipe_id])
    
    return render_template("recipe.html", recipe=recipe, categories=categories, reviews=reviews)



@app.route("/add_review/<int:recipe_id>", methods=["POST"])
def add_review(recipe_id):
    if "user_id" not in session:
        return redirect("/login")
    
    comment = request.form["comment"]
    rating = request.form["rating"]
    user_id = session["user_id"]
    
    if not comment or not rating:
        flash("Kommentti ja arvosana vaaditaan")
        return redirect(f"/recipe/{recipe_id}")
    
    check_sql = "SELECT id FROM recipes WHERE id = ?"
    result = db.query(check_sql, [recipe_id])
    
    if not result:
        flash("Reseptiä ei löytynyt")
        return redirect("/")
    
    insert_sql = "INSERT INTO reviews (recipe_id, user_id, comment, rating) VALUES (?, ?, ?, ?)"
    db.execute(insert_sql, [recipe_id, user_id, comment, rating])
    
    flash("Arvostelu lisätty onnistuneesti")
    return redirect(f"/recipe/{recipe_id}")


@app.route("/user/<int:user_id>")
def user_profile(user_id):
    user_sql = "SELECT username FROM users WHERE id = ?"
    result = db.query(user_sql, [user_id])
    
    if not result:
        flash("Käyttäjää ei löytynyt")
        return redirect("/")
    
    user = result[0]
    
    count_sql = "SELECT COUNT(*) as count FROM recipes WHERE user_id = ?"
    count_result = db.query(count_sql, [user_id])
    recipe_count = count_result[0]["count"]
    
    recipes_sql = "SELECT id, title, content FROM recipes WHERE user_id = ? ORDER BY id DESC"
    user_recipes = db.query(recipes_sql, [user_id])
    
    return render_template("user.html", user=user, recipe_count=recipe_count, user_recipes=user_recipes)


@app.route("/register", methods=["GET", "POST"])
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
                flash(f"Tervetuloa {username}!")
                return redirect("/")
        
        flash("Väärä tunnus tai salasana")
        return render_template("login.html")


@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
    if "username" in session:
        del session["username"]
    flash("Olet kirjautunut ulos")
    return redirect("/")


@app.route("/search")
def search():
    query = request.args.get("query", "")
    if query:
        sql = "SELECT r.id, r.title, r.content, u.username FROM recipes r, users u WHERE r.user_id = u.id AND (r.title LIKE ? OR r.content LIKE ?) ORDER BY r.id DESC"
        search_pattern = f"%{query}%"
        recipes = db.query(sql, [search_pattern, search_pattern])
    else:
        recipes = []
    
    return render_template("search.html", recipes=recipes, query=query)


@app.route("/categories")
def categories():
    categories_sql = "SELECT c.name, COUNT(rc.recipe_id) as recipe_count FROM categories c LEFT JOIN recipe_categories rc ON c.id = rc.category_id GROUP BY c.id, c.name ORDER BY c.name"
    categories = db.query(categories_sql)
    return render_template("categories.html", categories=categories)



