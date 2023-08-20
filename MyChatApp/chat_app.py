from flask import Flask, render_template, request

import openai

# Set up OpenAI API credentials
openai.api_key = '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'

app = Flask(__name__)

# Global chat data
chat_data = {
    'chat_rooms': {},
    'users': {}
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_room', methods=['POST'])
def create_room():
    user_id = request.form['user_id']
    # Generate a unique room ID for each user
    room_id = user_id + '_room'
    chat_data['chat_rooms'][room_id] = []
    chat_data['users'][user_id] = room_id
    return room_id

@app.route('/chat_room/<room_id>')
def chat_room(room_id):
    if room_id not in chat_data['chat_rooms']:
        return "Invalid room ID"
    return render_template('chat_room.html', room_id=room_id)

@app.route('/get_chat_data', methods=['POST'])
def get_chat_data():
    room_id = request.form['room_id']
    if room_id not in chat_data['chat_rooms']:
        return "Invalid room ID"

    room_chat = chat_data['chat_rooms'][room_id]
    return {'chat': room_chat}

@app.route('/send_message', methods=['POST'])
def send_message():
    user_id = request.form['user_id']
    room_id = chat_data['users'][user_id]
    message = request.form['message']
    
    # Send user message to GPT-3 API
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=f"User: {message}\nBot:",
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7
    )
    
    bot_reply = response.choices[0].text.strip()
    
    # Add bot reply to the chat room
    chat_data['chat_rooms'][room_id].append(('Bot', bot_reply))
    
    return ''

if __name__ == '__main__':
    app.run(debug=True)