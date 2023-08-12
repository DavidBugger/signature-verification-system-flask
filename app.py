from flask import Flask, render_template, request, redirect, session, flash
import face_recognition
from database import insert_member, get_member_by_username

app = Flask(__name__)
app.secret_key = 'hello'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hardcoded admin credentials (replace with your actual admin credentials)
        admin_username = 'admin'
        admin_password = 'password'

        if username == admin_username and password == admin_password:
            session['logged_in'] = True
            flash('Login successful!', 'success')
            return redirect('/register')
        else:
            flash('Invalid credentials. Please try again.', 'error')

    return render_template('login.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if not session.get('logged_in'):
        return redirect('/login')

    if request.method == 'POST':
        # Get form data and save to the database
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        address = request.form['address']
        gender = request.form['gender']
        photo = request.files['photo']

        if not firstname or not lastname or not username or not address or not gender or not photo:
            flash('Please fill in all fields.', 'error')
        else:
            try:
                insert_member(firstname, lastname, username, address, gender, photo.read())
                flash('Member registered successfully!', 'success')
            except Exception as e:
                flash(f'An error occurred: {e}', 'error')

    return render_template('register.html')


@app.route('/verification', methods=['GET', 'POST'])
def verification():
    if not session.get('logged_in'):
        return redirect('/login')

    if request.method == 'POST':
        # Get the verification photo and match it with the database entry
        verification_photo = request.files['verification_photo']
        username = request.form['username']

        if not verification_photo or not username:
            flash('Please provide both username and verification photo.', 'error')
        else:
            member = get_member_by_username(username)

            if not member:
                flash('Member not found in the database.', 'error')
            else:
                if face_matching_algorithm(verification_photo.read(), member['photo']):
                    flash('Verification successful!', 'success')
                    return render_template('verification.html', member=member)
                else:
                    flash('Verification failed. Photo does not match.', 'error')

    return render_template('verification.html')


def face_matching_algorithm(verification_photo, stored_photo):
    # Load the face encodings for the verification photo
    verification_image = face_recognition.load_image_file(verification_photo)
    verification_face_encoding = face_recognition.face_encodings(verification_image)

    # Load the face encodings for the stored photo
    stored_image = face_recognition.load_image_file(stored_photo)
    stored_face_encoding = face_recognition.face_encodings(stored_image)

    # Check if there is a face detected in both images
    if len(verification_face_encoding) == 0 or len(stored_face_encoding) == 0:
        return False

    # Compare the face encodings and return True if they match, False otherwise
    return face_recognition.compare_faces([verification_face_encoding[0]], stored_face_encoding[0])[0]

if __name__ == '__main__':
    app.run(debug=True)
