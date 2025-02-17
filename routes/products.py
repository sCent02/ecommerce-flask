from flask import Blueprint, render_template, request, redirect, url_for
from models import Product, Category
from database import db
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = "static/uploads"

products_bp = Blueprint("products", __name__)

@products_bp.route("/products")
def get_products():
    # Get filter & sort parameters from URL query
    category_id = request.args.get("category_id")
    sort_by = request.args.get("sort")

    # Start with all products
    query = Product.query

    # Apply category filter if selected
    if category_id and category_id != "All":
        query = query.filter(Product.category_id == category_id)

    # Apply sorting
    if sort_by == "price_low":
        query = query.order_by(Product.price.asc())
    elif sort_by == "price_high":
        query = query.order_by(Product.price.desc())

    # Get final list of products
    products = query.all()

    # Fetch unique categories for dropdown
    #categories = db.session.query(Product.category).distinct()
    categories = Category.query.all()  # Fetch all categories for the dropdown

    return render_template("products.html", products=products, categories=categories)

@products_bp.route("/manage_products")
def manage_products():
    products = Product.query.all()
    return render_template("manage_products.html", products=products)

@products_bp.route("/add_product", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        category_id = request.form["category_id"]
        file = request.files["image"]

        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            image_url = filename
        else:
            image_url = "default.jpg"

        new_product = Product(name=name, price=price, category_id=category_id, image_url=image_url)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for("products.manage_products"))

    categories = Category.query.all()
    return render_template("add_product.html", categories=categories)

@products_bp.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == "POST":
        product.name = request.form["name"]
        product.price = request.form["price"]
        product.category_id = request.form["category_id"]
        
        file = request.files["image"]
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            product.image_url = filename

        db.session.commit()
        return redirect(url_for("products.manage_products"))

    categories = Category.query.all()
    return render_template("edit_product.html", product=product, categories=categories)

@products_bp.route("/delete_product/<int:product_id>")
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for("products.manage_products"))

@products_bp.route("/manage_categories")
def manage_categories():
    categories = Category.query.all()
    return render_template("manage_categories.html", categories=categories)

@products_bp.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        name = request.form["name"]

        if name.strip():
            new_category = Category(name=name.strip())
            db.session.add(new_category)
            db.session.commit()
        
        return redirect(url_for("products.manage_categories"))

    return render_template("add_category.html")

@products_bp.route("/edit_category/<int:category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)

    if request.method == "POST":
        category.name = request.form["name"].strip()
        db.session.commit()
        return redirect(url_for("products.manage_categories"))

    return render_template("edit_category.html", category=category)

@products_bp.route("/delete_category/<int:category_id>")
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)

    # Prevent deleting categories if products exist in them
    if Product.query.filter_by(category_id=category.id).count() > 0:
        return "Cannot delete category with products", 400

    db.session.delete(category)
    db.session.commit()
    return redirect(url_for("products.manage_categories"))