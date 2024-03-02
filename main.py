import os
import tempfile
from flask import Flask, request, jsonify, send_file
from google.cloud import vision
from google.cloud import texttospeech

# Set up Google Cloud credentials
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./truvision-416017-6ac5fc6efb38.json"

app = Flask(__name__)

@app.route('/detect_text', methods=['POST'])
def detect_text():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    language = request.args.get('language', 'en-US')  # Get language parameter, default to English if not provided
    
    if file:
        client = vision.ImageAnnotatorClient()
        content = file.read()
        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations
        
        if texts:
            detected_text = texts[0].description
            audio_content = generate_audio(detected_text, language)
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                temp_file.write(audio_content)
                temp_file.flush()
                return send_file(temp_file.name, mimetype='audio/mpeg', as_attachment=True)
        else:
            return jsonify({'error': 'No text detected'}), 400
    else:
        return jsonify({'error': 'File upload failed'}), 400


def generate_audio(text, language):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language, ssml_gender=texttospeech.SsmlVoiceGender.MALE
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response.audio_content


if __name__ == '__main__':
    app.run(debug=True)
