from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dictionary to store reserved seats for each coach
reserved_seats = {
    1: [],  # Coach 1 reserved seats
    2: [],  # Coach 2 reserved seats
    3: [],  # Coach 3 reserved seats
    4: [],  # Coach 4 reserved seats
    5: [],  # Coach 5 reserved seats
    6: []   # Coach 6 reserved seats
}

# Configuration for each coach: (total_seats, seats_per_column)
coach_config = {
    1: (40, 10),  # Coach 1: 40 seats, 10 per column (2 columns on left)
    2: (40, 10),  # Coach 2: 40 seats, 10 per column (2 columns on left)
    3: (36, 9),   # Coach 3: 36 seats, 9 per column (4 columns)
    4: (32, 8),   # Coach 4: 32 seats, 8 per column (4 columns)
    5: (20, 10),  # Coach 5: 20 seats, 10 per column (2 rows)
    6: (16, 8)    # Coach 6: 16 seats, 8 per column (2 rows)
}


@app.route('/')
def seat_selection():
    coach = request.args.get('coach', 1, type=int)  # Get the current coach number, default is 1
    total_seats, seats_per_column = coach_config[coach]  # Get the configuration for the current coach
    seats = list(range(1, total_seats + 1))  # Create a list of seat numbers
    reserved = reserved_seats.get(coach, [])  # Get the reserved seats for the current coach
    num_columns = total_seats // seats_per_column  # Calculate the number of columns
    return render_template('seat_selection.html', seats=seats, coach=coach, reserved=reserved, num_columns=num_columns, seats_per_column=seats_per_column)

@app.route('/confirm', methods=['POST'])
def confirm_seat():
    selected_seat = request.form.get('seat')
    coach = request.form.get('coach', type=int)
    
    if not selected_seat:
        return redirect(url_for('seat_selection', coach=coach))  # Redirect if no seat selected

    selected_seat = int(selected_seat)  # Convert the selected seat to integer

    if selected_seat in reserved_seats[coach]:
        return redirect(url_for('seat_selection', coach=coach))  # Redirect if seat is already reserved
    
    reserved_seats[coach].append(selected_seat)  # Reserve the seat
    
    return render_template('ticket.html', seat=selected_seat, coach=coach)

if __name__ == '__main__':
    app.run(debug=True)


