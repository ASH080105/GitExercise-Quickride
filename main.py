from flask import Flask, redirect, url_for, session, render_template, request, flash
from functools import wraps
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management
app.permanent_session_lifetime = timedelta(minutes=30)  # Session timeout set to 30 minutes

# In-memory user storage for login/signup
users = {}

# Dictionary to store reserved seats for each coach
reserved_seats = {
    1: [],  # Coach 1 reserved seats
    2: [],  # Coach 2 reserved seats
    3: [],  # Coach 3 reserved seats
    4: [],  # Coach 4 reserved seats
    5: [],  # Coach 5 reserved seats
    6: []   # Coach 6 reserved seats
}

# Configuration for each coach: (total_seats, seats_per_column, seat_price)
coach_config = {
    1: (40, 10, 0),  # Coach 1: 40 seats, 10 per column, no extra charge
    2: (40, 10, 0),  # Coach 2: 40 seats, 10 per column, no extra charge
    3: (36, 9, 10),  # Coach 3: 36 seats, 9 per column, RM10 extra
    4: (32, 8, 15),  # Coach 4: 32 seats, 8 per column, RM15 extra
    5: (20, 10, 20), # Coach 5: 20 seats, 10 per column, RM20 extra
    6: (16, 8, 25)   # Coach 6: 16 seats, 8 per column, RM25 extra
}

# Decorator to ensure user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('You need to log in first', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Route for homepage
@app.route('/')
def home():
    return render_template('index.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username] == password:
            session['username'] = username  # Store username in session
            session.permanent = True  # Make session permanent
            flash('Successfully logged in!', 'success')
            return redirect(url_for('homepage'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

# Homepage route after login
@app.route('/homepage')
@login_required
def homepage():
    return render_template('homepage.html')

# Logout route
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
        elif username in users:
            flash('Username already exists', 'error')
        else:
            users[username] = password
            flash('Account created successfully!', 'success')
            return redirect(url_for('login'))
    
    return render_template('signup.html')

# Booking submission from homepage
@app.route('/submit-booking', methods=['POST'])
@login_required
def submit_booking():
    # Store booking information in session
    session['origin'] = request.form['origin']
    session['destination'] = request.form['destination']
    session['travel_date'] = request.form['travel-date']
    session['departure_time'] = request.form['departure-time']
    session['age_category'] = request.form['age-category']
    session['price'] = calculate_price(
        session['origin'],
        session['destination'],
        session['age_category']
    )
    
    # Redirect to seat selection after booking info is submitted
    return redirect(url_for('seat_selection'))

# Function to calculate price based on form input
def calculate_price(origin, destination, age_category):
    STATIONS_LIST = [
        "Alor Setar", "Anak Bukit", "Gurun", "Sungai Petani", 
        "Arau", "Padang Besar", "Jerantut", "Kampung Berkam", 
        "Kuala Lipis", "Batu Gajah", "Ipoh", "Kampar", 
        "Kuala Kangsar", "Slim River", "Sungkai", "Taiping", 
        "Nilai", "Seremban", "Kajang", "Rawang", "Sungai Buloh", 
        "Batang Melaka", "KL Sentral", "Kuala Lumpur", 
        "Segamat", "JB Sentral", "Gua Musang", "Pasir Mas", 
        "Bukit Mertajam", "Butterworth"
    ]
    
    origin_index = STATIONS_LIST.index(origin)
    destination_index = STATIONS_LIST.index(destination)
    
    # Calculate number of stations between origin and destination
    number_of_stations = abs(destination_index - origin_index)
    
    # Base price: RM 2 per station
    price = number_of_stations * 2

    # Apply discount based on age category
    if age_category == "student":
        price *= 0.5  # 50% discount for students
    elif age_category == "senior":
        price *= 0.4  # 60% discount for senior citizens
    
    return price

# Seat selection route
@app.route('/seat-selection')
@login_required
def seat_selection():
    coach = request.args.get('coach', 1, type=int)
    total_seats, seats_per_column, seat_price = coach_config[coach]
    seats = list(range(1, total_seats + 1))
    reserved = reserved_seats.get(coach, [])
    num_columns = total_seats // seats_per_column
    
    return render_template(
        'seat_selection.html',
        seats=seats,
        coach=coach,
        reserved=reserved,
        num_columns=num_columns,
        seats_per_column=seats_per_column,
        seat_price=seat_price,  # Pass the seat price
        origin=session.get('origin'),
        destination=session.get('destination'),
        travel_date=session.get('travel_date'),
        departure_time=session.get('departure_time'),
        price=session.get('price')
    )

# Route for confirming seat reservation
@app.route('/confirm', methods=['POST'])
@login_required
def confirm_seat():
    selected_seat = request.form.get('seat')
    coach = request.form.get('coach', type=int)
    
    if not selected_seat:
        flash('No seat selected', 'error')
        return redirect(url_for('seat_selection', coach=coach))
    
    selected_seat = int(selected_seat)
    
    if selected_seat in reserved_seats[coach]:
        flash('Seat already reserved', 'error')
        return redirect(url_for('seat_selection', coach=coach))
    
    reserved_seats[coach].append(selected_seat)
    
    # Get the base price and seat price
    seat_price = coach_config[coach][2]
    total_price = session.get('price', 0) + seat_price  # Base price + seat price
    
    flash(f'Seat {selected_seat} in coach {coach} successfully reserved!', 'success')
    
    return render_template(
        'ticket.html',
        seat=selected_seat,
        coach=coach,
        origin=session.get('origin'),
        destination=session.get('destination'),
        travel_date=session.get('travel_date'),
        departure_time=session.get('departure_time'),
        total_price=total_price  # Pass total price to the ticket template
    )

if __name__ == '__main__':
    app.run(debug=True)
