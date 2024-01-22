import logging
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import re
import long_responses as long
import openai
from openai.error import RateLimitError, InvalidRequestError, AuthenticationError
from api_secrets import OPENAI_API_KEY
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from pymongo import MongoClient
from datetime import datetime
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Use SQLite for simplicity
app.config['SECRET_KEY'] = '230cfd33beee0ce2e1f0078736c6a4e0'  # Change this to a secure random key
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

openai.api_key = OPENAI_API_KEY

# Connect to MongoDB
app.config['MONGO_URI'] = 'mongodb+srv://romanobrookswork:Miy3kvcUxwlKvQKx@cluster0.2ilgwz7.mongodb.net/cluster0'
mongo = PyMongo(app)

unanswered_count = 0
MAX_UNANSWERED_COUNT = 3

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_user(username, password):
    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(username=username, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

def check_user_credentials(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        return user

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    percentage = float(message_certainty) / float(len(recognised_words))

    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0

def check_all_messages(message):
    highest_prob_list = {}

    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    response('Hello!', ['hello', 'hi', 'hey', 'sup', 'heyo'], single_response=True)
    response('See you!', ['bye', 'goodbye'], single_response=True)
    response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
    response('You\'re welcome!', ['thank', 'thanks'], single_response=True)
    response('Thank you!', ['i', 'love', 'code', 'palace'], required_words=['code', 'palace'])

    # Longer responses
    response(long.R_ADVICE, ['give', 'advice'], required_words=['advice'])
    response(long.R_EATING, ['what', 'you', 'eat'], required_words=['you', 'eat'])

    if not highest_prob_list:
        # No recognized words or none of the predefined responses matched
        return long.unknown()

    best_match = max(highest_prob_list, key=highest_prob_list.get)

    global unanswered_count

    if highest_prob_list[best_match] < 1:
        unanswered_count += 1
        if unanswered_count >= MAX_UNANSWERED_COUNT:
            return openai_chatbot(' '.join(message))
    else:
        unanswered_count = 0

    return best_match

def openai_chatbot(user_input):
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=user_input,
            max_tokens=50
        )
        return response.choices[0].text.strip()
    except RateLimitError as e:
        return str(e)
    except InvalidRequestError as e:
        return str(e)
    except AuthenticationError as e:
        return str(e)

def log_to_mongo(sender, message, responder, response):
    timestamp = datetime.utcnow()
    log_entry = {
        'timestamp': timestamp,
        'sender': sender,
        'message': message,
        'responder': responder,
        'response': response
    }
    # Access the 'logs' collection in the MongoDB database
    mongo_collection = mongo.db.logs
    # Insert the log entry into the MongoDB collection
    mongo_collection.insert_one(log_entry)

@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_input = request.json.get("user_input")
        response = check_all_messages(re.split(r'\s+|[,;?!.-]\s*', user_input.lower()))

        # Log the conversation to MongoDB
        sender = 'user'
        responder = 'bot'
        log_to_mongo(sender, user_input, responder, response)

        return jsonify({"response": response})
    return render_template("chat.html", user_input="", response="")

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Invalid registration data"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 400

    create_user(username, password)
    return jsonify({"message": "Registration successful"})

@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        data = request.json
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"message": "Invalid login data"}), 400

        user = check_user_credentials(username, password)
        if user:
            login_user(user)
            return jsonify({"message": "Login successful"})
        else:
            return jsonify({"message": "Invalid username or password"}), 401

# Endpoint to display logs
@app.route("/logs")
def logs():
    # Access the 'logs' collection in the MongoDB database
    mongo_collection = mongo.db.logs
    # Fetch all logs from the collection
    logs = mongo_collection.find()

    # Aggregate message counts for each sender and responder
    pipeline = [
        {"$group": {"_id": "$sender", "sender_count": {"$sum": 1}, "responder": {"$first": "$responder"}}},
        {"$project": {"_id": 0, "sender": "$_id", "sender_count": 1, "responder": 1}},
        {"$sort": {"sender_count": -1}}
    ]
    message_counts = list(mongo_collection.aggregate(pipeline))

    return render_template("logs.html", logs=logs, message_counts=message_counts)

if __name__ == "__main__":
    app.run(debug=True)
