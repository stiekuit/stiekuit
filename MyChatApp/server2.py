import gradio as gr
import openai
import mysql.connector

# Set up MySQL connection
db = mysql.connector.connect(
    host='127.0.0.1',
    user='dbuser',
    password='Tesst123$$',
    database='users'
)

# Set your OpenAI API key


# Define the chatbot function
def openai_chatbot(user_input):
    response = openai.Completion.create(
        engine="davinci",
        prompt=user_input,
        max_tokens=50
    )
    return response.choices[0].text.strip()

# Define the Gradio prediction function
def predict_chatbot(input_text):
    # If input_text is a command, handle user registration
    if input_text.lower() == "/register":
        return "Please provide a username and password in the format '/register username password'."

    # Process user registration
    if input_text.lower().startswith("/register"):
        _, username, password = input_text.split()
        
        cursor = db.cursor()
        cursor.execute("INSERT INTO Users (Username, Password) VALUES (%s, %s)", (username, password))
        db.commit()

        return f"User {username} registered successfully!"

    # If not a command, proceed with chatbot interaction
    response = openai_chatbot(input_text)
    return response

# Define the Gradio interface
iface = gr.Interface(
    fn=predict_chatbot,
    inputs=gr.inputs.Textbox(),
    outputs=gr.outputs.Textbox(),
    title="OpenAI Chatbot"
)

# Launch the Gradio interface
iface.launch()

