from flask import Blueprint, redirect, render_template, request, session, flash
import db

categories_bp = Blueprint('categories', __name__)

@categories_bp.route("/categories")
def categories():
    categories_sql = """SELECT c.name, COUNT(rc.recipe_id) as recipe_count 
                        FROM categories c 
                        LEFT JOIN recipe_categories rc ON c.id = rc.category_id 
                        GROUP BY c.id, c.name 
                        ORDER BY c.name"""
    categories = db.query(categories_sql)
    return render_template("categories.html", categories=categories)