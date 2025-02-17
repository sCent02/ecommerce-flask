from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # ✅ Correct way to initialize SQLAlchemy

# Make sure DATABASE_URL is defined at the top level
DATABASE_URL = "sqlite:///products.db"  # Use PostgreSQL if needed