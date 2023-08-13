
from flask import Flask, render_template, request, jsonify
import imageio
from skimage.metrics import structural_similarity as ssim
from flask import Blueprint, render_template, request, jsonify
from skimage.metrics import structural_similarity as ssim


app = Flask(__name__)
verification_routes = Blueprint('verification_routes', __name__)
@verification_routes.route('/')
@verification_routes.route('/verification', methods=['GET', 'POST'])
@app.route('/verification', methods=['GET', 'POST'])
def verify_signature():
    if request.method == 'POST':
        genuine_signature = request.files['genuine_signature']
        forged_signature = request.files['forged_signature']

        similarity_percentage = simulate_signature_verification(genuine_signature, forged_signature)
        
        return jsonify({'similarity_percentage': similarity_percentage})
    
    return render_template('verify_signature.html')

def simulate_signature_verification(genuine_signature, forged_signature):
    genuine_image = imageio.imread(genuine_signature)
    forged_image = imageio.imread(forged_signature)
    
    similarity = ssim(genuine_image, forged_image, multichannel=True)
    similarity_percentage = similarity * 100
    
    return similarity_percentage


