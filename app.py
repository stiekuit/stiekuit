from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("chatbot.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.json["user_input"]
    bot_response = simple_chatbot(user_input)  # Use the chatbot function from the previous example
    return jsonify({"response": bot_response})

def simple_chatbot(user_input):
    # Your chatbot logic here (same as in the previous example)
    # ...

    if __name__ == "__main__":
        app.run(debug=True)
