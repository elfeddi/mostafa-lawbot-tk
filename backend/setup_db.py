from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db
from app.models import User


# Configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DXC_RAG.db'  # Update with your DB credentials
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Function to create the database and tables
def setup_database():
    with app.app_context():
        db.create_all()
        print("Database and tables created successfully.")

if __name__ == '__main__':
    setup_database()
