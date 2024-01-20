import logging
from flask import Flask, request, jsonify, render_template
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

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    # Counts how many words are present in each predefined message
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # Calculates the percent of recognised words in a user message
    percentage = float(message_certainty) / float(len(recognised_words))

    # Checks that the required words are in the string
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    # Must either have the required words, or be a single response
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

    best_match = max(highest_prob_list, key=highest_prob_list.get)

    return long.unknown() if highest_prob_list[best_match] < 1 else best_match

@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_input = request.json.get("user_input")
        response = check_all_messages(re.split(r'\s+|[,;?!.-]\s*', user_input.lower()))
        return jsonify({"response": response})
    return render_template("chat.html", user_input="", response="")

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
