from flask import Flask, render_template, request, jsonify
import openai
from openai.error import RateLimitError, InvalidRequestError
from api_secrets import OPENAI_API_KEY

app = Flask(__name__)

openai.api_key = OPENAI_API_KEY

def openai_chatbot(user_input):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_input,
            max_tokens=50
        )
        return response.choices[0].text.strip()
    except RateLimitError as e:
        return str(e)
    except InvalidRequestError as e:
        return str(e)

@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        user_input = request.json.get("user_input")
        response = openai_chatbot(user_input)
        return jsonify({"response": response})
    return render_template("chatbot.html", user_input="", response="")

if __name__ == "__main__":
    app.run(debug=False)
