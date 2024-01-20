import logging
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
import re

app = Flask(__name__)

# Configure logging to write to a file
logging.basicConfig(filename='chat_app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Dummy class for long responses
class LongResponses:
    def unknown(self):
        return "Sorry, I didn't understand that."

    # Add your long responses here
    R_ADVICE = "Sure, here's some advice: ..."
    R_EATING = "I don't eat, but I can suggest some recipes!"

long = LongResponses()

# Flask configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Use SQLite for simplicity
app.config['SECRET_KEY'] = '230cfd33beee0ce2e1f0078736c6a4e0'  # Change this to a secure random key
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_user(username, password):
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = User(username=username, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

def check_user_credentials(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        return user
    return None

# Your existing message processing functions
# ...

# Your existing routes
# ...

# New route for user registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Invalid registration data"}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "Username already exists"}), 409

    create_user(username, password)
    return jsonify({"message": "Registration successful"}), 200

if __name__ == '__main__':
    app.run(debug=True)
