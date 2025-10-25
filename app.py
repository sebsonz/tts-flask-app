from flask import Flask, request, jsonify, send_from_directory
from gtts import gTTS
import os
import uuid

app = Flask(__name__, static_folder="frontend", template_folder="frontend")

# Dossier pour audio dans STCATIC afin d'être servi par Render
AUDIO_FOLDER = os.path.join(app.static_folder, "audio")
os.makedirs(AUDIO_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/speak", methods=["POST"])
def speak():
    data = request.get_json()
    text = data.get("text")

    if not text:
        return jsonify({"error": "No text"}), 400

    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(AUDIO_FOLDER, filename)

    try:
        tts = gTTS(text=text, lang="fr")
        tts.save(filepath)

        # ✅ URL accessible publiquement
        audio_url = f"/static/audio/{filename}"
        return jsonify({"audioUrl": audio_url})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
