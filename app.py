from flask import Flask, render_template, request, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from skimage.metrics import structural_similarity as ssim
import sqlite3
import os
from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.applications import MobileNetV2
# from keras.applications import preprocess_input



app = Flask(__name__)
# model = tf.keras.models.load_model('model/pretrained_signature_model.h5')
app.secret_key = 'hello'  # Set your own secret key
# Connect to the SQLite database
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()
# Create the users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

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

 # Load your model here
model = tf.keras.models.load_model('model\pretrained_signature_model_full.h5') 
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        uploaded_file = request.files['signature']
        if uploaded_file.filename != '':
            image = process_uploaded_image(uploaded_file)
            prediction = predict_image(image)
            result = "Genuine" if prediction == 0 else "Forged"
            return jsonify({'prediction': prediction, 'result': result})
        return jsonify({'prediction': -1, 'result': 'No file uploaded'})
    return render_template('verify.html')

def process_uploaded_image(uploaded_file):
    image = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)
    image = cv2.resize(image, (224, 224))
    image = image / 255.0
    return image

def predict_image(image):
    tensor = model.predict(np.expand_dims(image, axis=0))
    distance = np.sum(np.square(tensor - tensor), axis=-1)
    prediction = 0 if np.any(distance <= 0.85) else 1
    return prediction







# from keras.models import load_model

# Load the model
# model = tf.keras.models.load_model('model/encoder.h5')

# def classify_images(face_list1, face_list2, threshold=0.85):
#     tensor1 = model.predict(face_list1)
#     tensor2 = model.predict(face_list2)
    
#     distance = np.sum(np.square(tensor1 - tensor2), axis=-1)
#     prediction = np.where(distance <= threshold, 0, 1)
#     return prediction

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         uploaded_files = request.files.getlist("file")
        
#         if len(uploaded_files) == 2:
#             images = [cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_COLOR) for file in uploaded_files]
#             images = [cv2.resize(img, (256, 256)) for img in images]
#             images = [keras.applications.preprocess_input(img) for img in images]
#             distance = classify_images(np.expand_dims(images[0], axis=0), np.expand_dims(images[1], axis=0))
            
#             return jsonify({"distance": distance[0]})
            
#     return render_template('verify.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect('/')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
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

    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
