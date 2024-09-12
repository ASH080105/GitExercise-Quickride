from . import db
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from sqlalchemy .sql import func

class Origin(db.Model, UserMixin):
    id = db.Column(db.integer, primary_key=True)
    city_station = db.Column(db.string(120))
    date = db.Column(db.date)
    number_of_pax = db.Column(db.integer, nullable=False)
    time = db.Column(db.time)

class Booking(db.Model):
    id = db.Column(db.integer, primary_key=True)
    user_id= db.Column(db.integer, db.ForeignKey('user.id'), nullable=False)
    customer_name = db.Column(db.String(140), nullable=False)
    total_price =  db.Column(db.integer, nullable=False)
    number_of_pax = db.Column(db.integer, nullable=False)
    Booking_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.relationship('User', backref="bookings")

    
      
    