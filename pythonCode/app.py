from flask import Flask, request, jsonify
from characterai import PyCAI
import requests
app = Flask(__name__)
# Initialize the Character.ai client
character_ai_client = PyCAI('a5c2f69274c87103925b32bd67ed45cff0b15957')

@app.route('/')
def hello_world():
    return 'Hello, World!'
@app.route('/get_text', methods=['POST'])
def get_text():
    # Handle Character.ai API request here
    # Return the obtained text as JSON
    pass
@app.route('/start_chat', methods=['POST'])
def start_chat():
    data = request.json
    char = data.get('char', '').lower()

    if char == 'father':
        char = 'uMnXQwm3ii7GGQUUExv4yfu4v_2_wYec4u-7K3H6Mbw'

    chat = character_ai_client.chat.get_chat(char)
    participants = chat['participants']

    if not participants[0]['is_human']:
        tgt = participants[0]['user']['username']
    else:
        tgt = participants[1]['user']['username']

    return jsonify({'tgt': tgt, 'chat_external_id': chat['external_id']})

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    chat_external_id = data.get('chat_external_id')
    tgt = data.get('tgt')
    message = data.get('message')

    data = character_ai_client.chat.send_message(chat_external_id, tgt, message)

    name = data['src_char']['participant']['name']
    text = data['replies'][0]['text']

    return jsonify({'name': name, 'text': text})

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/generate_video', methods=['POST'])
def generate_video():
    # Handle d-id API request here
    # Return the video or a link to the generated video
    pass

if __name__ == '__main__':
    # Run the Flask app using Gunicorn from the command line
    # Example command: gunicorn -w 4 -b 0.0.0.0:5000 your_app_module:app
    import os
    os.system('gunicorn -w 4 -b 0.0.0.0:5000 app:app')
