from app import app, db
from models import Product, Category

with app.app_context():
    category = Category.query.first()
    if not category:
        category = Category(name="Electronics")
        db.session.add(category)
        db.session.commit()

    product = Product.query.filter_by(name="Laptop").first()
    if product:
        product.image_url = "Laptop.jpeg"  # ✅ Update existing product
        print("✅ Updated existing product image.")
    else:
        product = Product(
            name="Laptop",
            price=999.99,
            category_id=category.id,
            image_url="Laptop.jpeg"
        )
        db.session.add(product)
        print("✅ Added new product.")

    db.session.commit()