from flask import Flask, request, jsonify, send_from_directory
from gtts import gTTS
import os
import uuid

app = Flask(__name__, static_folder="frontend", template_folder="frontend")

AUDIO_FOLDER = "static/audio"
os.makedirs(AUDIO_FOLDER, exist_ok=True)


@app.route('/')
def index():
    return send_from_directory("frontend", "index.html")


@app.route('/speak', methods=['POST'])
def speak():
    data = request.get_json()
    text = data.get("text")

    if not text:
        return jsonify({"error": "Texte manquant"}), 400

    try:
        filename = f"{uuid.uuid4()}.mp3"
        filepath = os.path.join(AUDIO_FOLDER, filename)

        tts = gTTS(text=text, lang="fr")
        tts.save(filepath)

        return jsonify({"audioUrl": f"/static/audio/{filename}"})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/<path:filename>')
def frontend_files(filename):
    return send_from_directory("frontend", filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
