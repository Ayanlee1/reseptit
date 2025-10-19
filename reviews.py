from flask import Blueprint, redirect, render_template, request, session, flash
import db
from auth import login_required, check_csrf

reviews_bp = Blueprint('reviews', __name__)


@reviews_bp.route("/add_review/<int:recipe_id>", methods=["POST"])
@login_required
def add_review(recipe_id):
    check_csrf()
    
    comment = request.form["comment"]
    rating = request.form["rating"]
    user_id = session["user_id"]
    
    if not comment or not rating:
        flash("Kommentti ja arvosana vaaditaan")
        return redirect(f"/recipe/{recipe_id}")
        
    if len(comment) > 1000:
        flash("Kommentti on liian pitkä (max 1000 merkkiä)")
        return redirect(f"/recipe/{recipe_id}")
    
    check_sql = "SELECT id FROM recipes WHERE id = ?"
    result = db.query(check_sql, [recipe_id])
    
    if not result:
        flash("Reseptiä ei löytynyt")
        return redirect("/")
    
    existing_sql = "SELECT id FROM reviews WHERE recipe_id = ? AND user_id = ?"
    existing = db.query(existing_sql, [recipe_id, user_id])
    
    if existing:
        flash("Olet jo arvostellut tämän reseptin")
        return redirect(f"/recipe/{recipe_id}")
    
    insert_sql = "INSERT INTO reviews (recipe_id, user_id, comment, rating) VALUES (?, ?, ?, ?)"
    db.execute(insert_sql, [recipe_id, user_id, comment, rating])
    
    flash("Arvostelu lisätty onnistuneesti")
    return redirect(f"/recipe/{recipe_id}")