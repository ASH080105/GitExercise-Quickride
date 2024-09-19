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

    


    




if __name__ == "__main__":
    app.run(debug=True)
    