from flask import Flask, render_template, request, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from skimage.metrics import structural_similarity as ssim
import imageio
import sqlite3
import os
import random
import string
from flask import jsonify

app = Flask(__name__)
app.secret_key = 'hello'  # Set your own secret key
app.config['UPLOAD_FOLDER'] = 'static/photos'

# Connect to the SQLite database
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

# Create the users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        firstname TEXT NOT NULL,
        lastname TEXT NOT NULL,
        address TEXT NOT NULL,
        photo TEXT NOT NULL,
        gender TEXT NOT NULL,
        criminal_offence TEXT NOT NULL,
        status TEXT NOT NULL,
        nationality TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS register_members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        firstname TEXT NOT NULL,
        lastname TEXT NOT NULL,
        address TEXT NOT NULL,
        photo TEXT NOT NULL,
        gender TEXT NOT NULL,
        criminal_offence TEXT NOT NULL,
        status TEXT NOT NULL,
        nationality TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

# Insert an initial admin user
username = 'admin'
password = 'admin'
role = 'admin'

# Check if the admin user already exists
cursor.execute("SELECT * FROM users WHERE username=?", (username,))
admin_user = cursor.fetchone()

if not admin_user:
    # If the admin user doesn't exist, insert it into the users table
    hashed_password = generate_password_hash(password)
    cursor.execute("INSERT INTO register_members (username, firstname, lastname, address, photo, gender, criminal_offence, status, nationality, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (username, '', '', '', '', '', '', '', '', hashed_password))
    conn.commit()
    
    
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[2], password):
            session['username'] = user[1]
            session['role'] = user[3]
            flash('Login successful!', 'success')
            return redirect('/dashboard')

        flash('Invalid username or password', 'error')

    return render_template('login.html')


@app.route('/verification', methods=['GET', 'POST'])
def verify_signature():
    if request.method == 'POST':
        genuine_signature = request.files['genuine_signature']
        forged_signature = request.files['forged_signature']

        similarity_percentage = simulate_signature_verification(genuine_signature, forged_signature)
        
        return jsonify({'similarity_percentage': similarity_percentage})
    
    return render_template('verify.html')

def simulate_signature_verification(genuine_signature, forged_signature):
    genuine_image = imageio.imread(genuine_signature)
    forged_image = imageio.imread(forged_signature)
    
    similarity = ssim(genuine_image, forged_image, multichannel=True)
    similarity_percentage = similarity * 100
    
    return similarity_percentage




def count_total_members():
    cursor.execute("SELECT COUNT(*) FROM register_members")
    total_members = cursor.fetchone()[0]
    return total_members

def count_members_with_criminal_records():
    cursor.execute("SELECT COUNT(*) FROM register_members WHERE criminal_offence = 'yes'")
    members_with_criminal_records = cursor.fetchone()[0]
    return members_with_criminal_records

def count_nigerian_members():
    cursor.execute("SELECT COUNT(*) FROM register_members WHERE nationality = 'Nigeria'")
    nigerian_members = cursor.fetchone()[0]
    return nigerian_members




@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect('/')

# Route for registering a new member
@app.route('/register_member', methods=['GET', 'POST'])
def register_member():
    if request.method == 'POST':
        # Get user details from the form
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        address = request.form['address']
        photo = request.files['photo']
        gender = request.form.get('gender')
        criminal_offence = request.form.get('criminal_offence')
        status = request.form.get('status')
        # nationality = request.form['nationality']
        # Get the selected nationality from the form
        nationality = request.form.get('nationality')


        # Save the uploaded photo file
        photo_filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))

        # Generate a random username (you can use any logic to generate a username)
        username = firstname.lower() + lastname.lower() 

        # Generate a random password (you can use any logic to generate a password)
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        # Hash the password before storing in the database
        hashed_password = generate_password_hash(password)

        # Insert user data into the database
        cursor.execute("INSERT INTO register_members (username, firstname, lastname, address, photo, gender, criminal_offence, status, nationality, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (username, firstname, lastname, address, photo_filename, gender, criminal_offence, status, nationality, hashed_password))
        conn.commit()
         # Display success message with SweetAlerts
        success_message = f'Registration successful! Username: {username}, Password: {password}'
        # Display success message with username and password
        flash(f'Registration successful! Username: {username}, Password: {password}', 'success')
          # Use SweetAlerts to show the success message
        return jsonify({'message': success_message})

    return render_template('register_member.html')


@app.route('/verify_member', methods=['GET','POST'])
def verify_member():
    if request.method == 'POST':
        username = request.form['username']
        # Fetch the member details from the database
        cursor.execute("SELECT * FROM register_members WHERE username = ?", (username,))
        member = cursor.fetchone()
        if member:
            # If the member exists, show the details in a modal
            return jsonify({'status': 'success', 'member': member})
        else:
            # If member doesn't exist, show an error message
            return jsonify({'status': 'error', 'message': 'Member not found'})
    return render_template('verify.html')
    


# Route to display registered member details
@app.route('/details')
def display_details():
    # Fetch all registered members from the database
    cursor.execute("SELECT * FROM register_members")
    members = cursor.fetchall()

    return render_template('details.html', members=members)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # Get the total number of registered members
    total_members = count_total_members()

    # Get the number of members with criminal records
    members_with_criminal_records = count_members_with_criminal_records()

    # Get the number of Nigerian members
    nigerian_members = count_nigerian_members()

    if 'username' not in session or session['role'] != 'admin':
        flash('Unauthorized access!', 'error')
        return redirect('/')

    if request.method == 'POST':
        member_username = request.form['member_username']

        cursor.execute("SELECT * FROM users WHERE username = ?", (member_username,))
        member = cursor.fetchone()

        if member:
            return render_template('modal.html', member=member)
        else:
            flash('Member not found!', 'error')

    return render_template('dashboard.html', total_members=total_members, members_with_criminal_records=members_with_criminal_records, nigerian_members=nigerian_members)

if __name__ == '__main__':
    app.run(debug=True)
