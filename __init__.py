from flask import Flask, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_admin import Admin

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask( __name__)
    app.config['SECRET_KEY'] = 'Secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqllite:///{DB_NAME}
    db.init_app()

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    # Import models to create tables
    from .model import Booking, Origin
    
    with app.app_context():
        db.create_all()  # Create database tables

    return app

# Optional: User loader for Flask-Login

def load_user(user_id):
    from .model import User  # Adjust the import based on your User model location
    return User.query.get(int(user_id))

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)




    




