import http.server
import socketserver
import json
import gradio as gr
import openai

# Set your OpenAI API key
OPENAI_API_KEY = "your_openai_api_key_here"
openai.api_key = OPENAI_API_KEY

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
