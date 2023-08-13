from flask import Flask, session
from routes import verification_routes  # Import the Blueprint from routes.py

app = Flask(__name__)
app.secret_key = 'hello'  # Set a secret key for session management

app.register_blueprint(verification_routes, url_prefix='')  # Register the blueprint from routes.py

if __name__ == '__main__':
    app.run(debug=True)
