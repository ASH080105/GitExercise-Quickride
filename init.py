from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "train_ticketing_system.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    from .model import Origin, Booking

    with app.app_context():
        db.create_all()
        insert_initial_data()  # Insert data after creating the tables

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

# Inserting data into table Origin
def insert_initial_data():
    from .model import Origin

    if Origin.query.first() is None:
        stations = [
            {"city_station": "Alor Setar", "date": "2024-01-01", "number_of_pax": 1, "time": "5:30 AM"},
            {"city_station": "Anak Bukit", "date": "2024-02-15", "number_of_pax": 2, "time": "6:00 AM"},
            {"city_station": "Gurun", "date": "2024-03-10", "number_of_pax":3, "time": "6:30 AM"},
            {"city_station": "Sungai Petani", "date": "2024-04-05", "number_of_pax": 4, "time": "7:00 AM"},
            {"city_station": "Arau", "date": "2024-05-18", "number_of_pax": 5, "time": "07:30 AM"},
            {"city_station": "Padang Besar", "date": "2024-06-27", "number_of_pax": 6, "time": "08:00 AM"},
            {"city_station": "Jerantut", "date": "2024-07-13", "number_of_pax": 7, "time": "8:30 AM"},
            {"city_station": "Kampung Berkam", "date": "2024-08-06", "number_of_pax": 8, "time": "9:00 AM"},
            {"city_station": "Kuala Lipis", "date": "2024-09-17", "number_of_pax": 9, "time": "9:30 AM"},
            {"city_station": "Batu Gajah", "date": "2024-10-30", "number_of_pax": 10, "time": "10:00 AM"},
            {"city_station": "Ipoh", "date": "2024-11-14", "number_of_pax": 1, "time": "10:30 AM"},
            {"city_station": "Kampar", "date": "2024-12-25", "number_of_pax": 2, "time": "11:00 AM"},
            {"city_station": "Kuala Kangsar", "date": "2025-01-04", "number_of_pax": 3, "time": "11:30 AM"},
            {"city_station": "Slim River", "date": "2025-02-19", "number_of_pax": 4, "time": "12:00 PM"},
            {"city_station": "Sungkai", "date": "2025-03-01", "number_of_pax": 5, "time": "12:30 PM"},
            {"city_station": "Taiping", "date": "2025-04-28", "number_of_pax": 6, "time": "1:00 PM"},
            {"city_station": "Nilai", "date": "2025-05-03", "number_of_pax": 7, "time": "1:30 PM"},
            {"city_station": "Seremban", "date": "2025-06-18", "number_of_pax": 8, "time": "2:00 PM"},
            {"city_station": "Kajang", "date": "2025-07-10", "number_of_pax": 9, "time": "2:30 PM"},
            {"city_station": "Rawang", "date": "2025-08-07", "number_of_pax": 10, "time": "3:00 PM"},
            {"city_station": "Sungai Buloh", "date": "2025-09-20", "number_of_pax": 1, "time": "11:30 PM"},
            {"city_station": "Batang Melaka", "date": "2025-10-11", "number_of_pax": 2, "time": "5:30 AM"},
            {"city_station": "KL Sentral", "date": "2025-11-08", "number_of_pax": 3, "time": "6:00 AM"},
            {"city_station": "Kuala Lumpur", "date": "2025-12-22", "number_of_pax": 4, "time": "6:30 AM"},
            {"city_station": "Segamat", "date": "2026-01-09", "number_of_pax": 5, "time": "7:00 AM"},
            {"city_station": "JB Sentral", "date": "2026-02-24", "number_of_pax": 6, "time": "7:30 AM"},
            {"city_station": "Gua Musang", "date": "2026-03-17", "number_of_pax": 7, "time": "8:00 AM"},
            {"city_station": "Pasir Mas", "date": "2026-04-18", "number_of_pax": 8, "time": "8:30 AM"},
            {"city_station": "Sri Bintang", "date": "2026-05-10", "number_of_pax": 9, "time": "9:00 AM"},
            {"city_station": "Bukit Mertajam", "date": "2026-06-25", "number_of_pax": 10, "time": "9:30 AM"},
            {"city_station": "Butterworth", "date": "2026-07-30", "number_of_pax": 1, "time": "10:00 AM"}
        ]

        for station in stations:
            origin = Origin(**station)
            db.session.add(origin)

    else:
        print("Data already exists, skipping insertion.")

    db.session.commit()



    




