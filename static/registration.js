import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configure logging to write to a file
logging.basicConfig(filename='chat_app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/registration', methods=['POST'])
def registration():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']

        # Your registration logic here

        # Log successful registration at the debug level
        logging.debug(f"Registration successful for username: {username}")

        return jsonify({"message": "Registration successful"}), 200
    except Exception as e:
        # Log errors at the error level
        logging.error(f"Error during registration: {str(e)}")
        return jsonify({"message": "Error during registration"}), 500

@app.route('/record-request', methods=['POST'])
def record_request():
    try:
        data = request.get_json()
        sender = data['sender']
        responder = data['responder']

        # Your record request logic here

        # Log the recorded request at the debug level
        logging.debug(f"Request recorded - Sender: {sender}, Responder: {responder}")

        return jsonify({"message": "Request recorded successfully"}), 200
    except Exception as e:
        # Log errors at the error level
        logging.error(f"Error recording request: {str(e)}")
        return jsonify({"message": "Error recording request"}), 500

if __name__ == '__main__':
    app.run(debug=True)
