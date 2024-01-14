# MyChatApp/chat_app.py
from flask import Flask, render_template, request

app = Flask(__name__)

def simple_chatbot(user_input):
    user_input = user_input.lower()
    
    if "hello" in user_input:
        return "Hello! How can I assist you?"
    elif "how are you" in user_input:
        return "I'm just a chatbot, but I'm here and ready to help!"
    elif "bye" in user_input:
        return "Goodbye! Have a great day!"
    else:
        return "I'm sorry, I don't understand that."

@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_input = request.form.get("user_input")
        response = simple_chatbot(user_input)
        return render_template("index.html", user_input=user_input, response=response)
    return render_template("index.html", user_input="", response="")

if __name__ == "__main__":
    app.run(debug=True)
