from datetime import datetime

from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
import Speech_To_Text as stt
import Translate as tr
import json

load_dotenv()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'aac', 'm4a'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@socketio.on('connect')
def test_connect():
    print('Client connected')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def process_audio_file(audio_file_path):
    if not os.path.exists(audio_file_path):
        print(f'Not valid path for input audio file! {audio_file_path}')
        return None

    # Original AUDIO
    #audio_data, sampling_rate = stt.read_mp3(audio_file_path)

    # Text HUN
    text_data_HUN = stt.audio_to_text_HUN(audio_file_path)

    # Text ENG
    text_data_ENG = tr.text_HUN_to_text_ENG(text_data_HUN)

    return text_data_HUN, text_data_ENG

@app.route('/send-data', methods=['POST'])
def receive_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        print('File ', filename, 'saved')

        tempAudioForTesting = 'uploads/'+filename

        print(tempAudioForTesting)
        text_data_HUN, text_data_ENG = process_audio_file(tempAudioForTesting)

        print(text_data_HUN)
        print(text_data_ENG)
        print('Success')

        response_data = {"hun": text_data_HUN,
                         "eng": text_data_ENG}

        socketio.emit('file_saved', {'filepath': file_path, 'data': response_data})

        return jsonify({'message': 'Audio uploaded successfully to' + filename})

    return jsonify({'error': 'Invalid file type'}), 400


DATA_FOLDER = './data'
@app.route('/submit-form', methods=['POST'])
def submit_form():
    try:
        form_datas = request.json
        name = form_datas.get('name')
        location = form_datas.get('location')
        form_data = form_datas.get('payload')
        editedHun = form_data.get('editedHun', '')

        words = editedHun.split()
        word_count = len(words)

        if word_count == 1:
            file_name_part = words[0]
        elif word_count in [2, 3]:
            file_name_part = '_'.join(words)
        else:
            file_name_part = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        
        index = 1
        file_name = os.path.join(DATA_FOLDER, f"{name}_{location}_{file_name_part}_{index}.json")
        while os.path.exists(file_name):
            index += 1
            file_name = os.path.join(DATA_FOLDER, f"{name}_{location}_{file_name_part}_{index}.json")

        
        with open(file_name, 'w') as file:
            json.dump(form_data, file, indent=4)

        return jsonify(message="Form data received successfully"), 200
    except Exception as e:
        print("Error: ", str(e))
        return jsonify(error=str(e)), 500


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    socketio.run(app, host='0.0.0.0', port=8000, debug=True)
