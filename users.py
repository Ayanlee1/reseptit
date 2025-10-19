from flask import Blueprint, redirect, render_template, request, session, flash
import db


users_bp = Blueprint('users', __name__)

@users_bp.route("/user/<int:user_id>")
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