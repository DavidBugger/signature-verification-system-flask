
from flask import Flask, render_template, request, jsonify,request, redirect, flash, session
import imageio
from skimage.metrics import structural_similarity as ssim
from flask import Blueprint, render_template, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
from skimage.metrics import structural_similarity as ssim


app = Flask(__name__)
verification_routes = Blueprint('verification_routes', __name__)
login = Blueprint('login', __name__)
@verification_routes.route('/')
@verification_routes.route('/verification', methods=['GET', 'POST'])
@app.route('/verification', methods=['GET', 'POST'])
def verify_signature():
    if request.method == 'POST':
        genuine_signature = request.files['genuine_signature']
        forged_signature = request.files['forged_signature']

        similarity_percentage = simulate_signature_verification(genuine_signature, forged_signature)
        
        return jsonify({'similarity_percentage': similarity_percentage})
    
    return render_template('index.html')

def simulate_signature_verification(genuine_signature, forged_signature):
    genuine_image = imageio.imread(genuine_signature)
    forged_image = imageio.imread(forged_signature)
    
    similarity = ssim(genuine_image, forged_image, multichannel=True)
    similarity_percentage = similarity * 100
    
    return similarity_percentage


# routes.py
@app.route("/login", methods=["POST"])
def login(request):
    # Extract username and password from the form data
    username = request.form.get("username")
    password = request.form.get("password")

    # Check if the provided username and password are valid
    if username == "user" and password == "password":
        return True
    else:
        return False

