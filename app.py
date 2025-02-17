import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from database import db, DATABASE_URL
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
db.init_app(app)  # ✅ Initialize db with the Flask app

# ✅ Import models AFTER initializing db to avoid circular imports
from models import Product, Category
from routes.products import products_bp

app.register_blueprint(products_bp)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)
            return redirect(url_for("uploaded_file", filename=filename))
    return render_template("upload.html")

from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # ✅ Ensures tables are created before running the app
    app.run(debug=True, host="0.0.0.0", port=5000)