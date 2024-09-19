from flask import Blueprint, render_template, request, redirect, flash, url_for
from . import create_app
from .model import Origin, Booking
from .import db
import datetime

views = Blueprint('views',__name__)

months = [
    {'value': '01', 'label': '01 - January'},
    {'value': '02', 'label': '02 - February'},
    {'value': '03', 'label': '03 - March'},
    {'value': '04', 'label': '04 - April'},
    {'value': '05', 'label': '05 - May'},
    {'value': '06', 'label': '06 - June'},
    {'value': '07', 'label': '07 - July'},
    {'value': '08', 'label': '08 - August'},
    {'value': '09', 'label': '09 - September'},
    {'value': '10', 'label': '10 - October'},
    {'value': '11', 'label': '11 - November'},
    {'value': '12', 'label': '12 - December'},

]

days = [
    {'value': '1', 'label': 'Sunday'},
    {'value': '2', 'label': 'Monday'},
    {'value': '3', 'label': 'Tuesday'},
    {'value': '4', 'label': 'Wednesday'},
    {'value': '5', 'label': 'Thursday'},
    {'value': '6', 'label': 'Friday'},
    {'value': '7', 'label': 'Saturday'},

]

id = request.args.get('id')
city_station = request.args.get('city station')
date = request.args.get('date')
number_of_pax = request.args.get('number_of_pax')
time = request.args.get('time')
user_id = request.args.get('user_id')
customer_name = request.args.get('customer_name')
total_price = request.args.get('total_price')
Booking_date = request.args.get('Booking_date')
user = request.args.get('user')


@views.route('/book-ticket', methods=['GET', 'POST'])
def book_ticket():
    # List of stations (assuming it's static for now, can be fetched from a database)
    stations = [
        "Alor Setar", "Anak Bukit", "Gurun", "Sungai Petani", "Arau", "Padang Besar",
        "Jerantut", "Kampung Berkam", "Kuala Lipis", "Batu Gajah", "Ipoh", "Kampar", 
        "Kuala Kangsar", "Slim River", "Sungkai", "Taiping", "Nilai", "Seremban", 
        "Kajang", "Rawang", "Sungai Buloh", "Batang Melaka", "KL Sentral", 
        "Kuala Lumpur", "Segamat", "JB Sentral", "Gua Musang", "Pasir Mas", "Sri Bintang", 
        "Bukit Mertajam", "Butterworth"
    ]
    
    if request.method == 'POST':
        origin = request.form.get('origin')
        destination = request.form.get('destination')
        departure_time = request.form.get('departure_time')
        arrival_time = request.form.get('arrival_time')
        pax = request.form.get('pax')
        
        if origin == destination:
            flash('Origin and destination cannot be the same.', category='error')
            return redirect(url_for('views.book_ticket'))

        
        if not origin or not destination or not departure_time or not arrival_time or not pax:
            flash('Please fill in all fields', category='error')
            return redirect(url_for('views.book_ticket'))
        
        
        new_booking = Booking(
            origin=origin,
            destination=destination,
            departure_time=departure_time,
            arrival_time=arrival_time,
            number_of_pax=pax,
            booking_date=datetime.datetime.now()
        )
        db.session.add(new_booking)
        db.session.commit()
        
        flash('Booking successful!', category='success')
        return redirect(url_for('views.ticket_history'))
    
    return render_template('book_ticket.html', stations=stations)





