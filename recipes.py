from flask import Blueprint, redirect, render_template, request, session, flash
import db
from auth import login_required, check_csrf


recipes_bp = Blueprint('recipes', __name__)


@recipes_bp.route("/new_recipe")
@login_required
def new_recipe():
    categories_sql = "SELECT id, name FROM categories ORDER BY name"
    categories = db.query(categories_sql)
    return render_template("new_recipe.html", categories=categories)


@recipes_bp.route("/create_recipe", methods=["POST"])
@login_required
def create_recipe():
    check_csrf()
    
    title = request.form["title"]
    content = request.form["content"]
    user_id = session["user_id"]
    
    if not title or not content:
        flash("Otsikko ja sisältö eivät voi olla tyhjiä")
        return redirect("/new_recipe")
        
    if len(title) > 100:
        flash("Otsikko on liian pitkä (max 100 merkkiä)")
        return redirect("/new_recipe")
        
    if len(content) > 5000:
        flash("Reseptin sisältö on liian pitkä (max 5000 merkkiä)")
        return redirect("/new_recipe")

    sql = "INSERT INTO recipes (title, content, user_id) VALUES (?, ?, ?)"
    recipe_id = db.execute(sql, [title, content, user_id])
    
    categories = request.form.getlist("categories")
    
    for category_id in categories:
        category_sql = "INSERT INTO recipe_categories (recipe_id, category_id) VALUES (?, ?)"
        db.execute(category_sql, [recipe_id, category_id])
    
    flash("Resepti lisätty onnistuneesti")
    return redirect("/")


@recipes_bp.route("/edit_recipe/<int:recipe_id>")
@login_required
def edit_recipe(recipe_id):
    sql = "SELECT id, title, content, user_id FROM recipes WHERE id = ?"
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


@recipes_bp.route("/update_recipe/<int:recipe_id>", methods=["POST"])
@login_required
def update_recipe(recipe_id):
    check_csrf()
    
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
        
    if len(title) > 100:
        flash("Otsikko on liian pitkä (max 100 merkkiä)")
        return redirect(f"/edit_recipe/{recipe_id}")
        
    if len(content) > 5000:
        flash("Reseptin sisältö on liian pitkä (max 5000 merkkiä)")
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


@recipes_bp.route("/delete_recipe/<int:recipe_id>", methods=["POST"])
@login_required
def delete_recipe(recipe_id):
    check_csrf()
    
    check_sql = "SELECT user_id FROM recipes WHERE id = ?"
    result = db.query(check_sql, [recipe_id])
    
    if not result or result[0]["user_id"] != session["user_id"]:
        flash("Voit poistaa vain omia reseptejäsi")
        return redirect("/")
    
    delete_sql = "DELETE FROM recipes WHERE id = ?"
    db.execute(delete_sql, [recipe_id])
    
    flash("Resepti poistettu onnistuneesti")
    return redirect("/")


@recipes_bp.route("/recipe/<int:recipe_id>")
def recipe_page(recipe_id):
    sql = """SELECT r.id, r.title, r.content, u.username, u.id as user_id 
             FROM recipes r, users u 
             WHERE r.id = ? AND r.user_id = u.id"""
    result = db.query(sql, [recipe_id])
    
    if not result:
        flash("Reseptiä ei löytynyt")
        return redirect("/")
    
    recipe = result[0]
    
    categories_sql = """SELECT c.name 
                        FROM categories c, recipe_categories rc 
                        WHERE rc.recipe_id = ? AND rc.category_id = c.id"""
    categories = db.query(categories_sql, [recipe_id])
    
    reviews_sql = """SELECT r.comment, r.rating, u.username 
                     FROM reviews r, users u 
                     WHERE r.recipe_id = ? AND r.user_id = u.id 
                     ORDER BY r.id DESC"""
    reviews = db.query(reviews_sql, [recipe_id])
    
    return render_template("recipe.html", recipe=recipe, categories=categories, reviews=reviews)