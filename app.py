from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your own secret key

# In-memory user storage
users = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username] == password:
            flash('Successfully logged in!', 'success')
            return redirect(url_for('success'))  # Redirect to a success page
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        
        if password != confirm_password:
            flash('Passwords do not match')
        elif username in users:
            flash('Username already exists')
        else:
            users[username] = password
            return redirect(url_for('login'))
    
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
