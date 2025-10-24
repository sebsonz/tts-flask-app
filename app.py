from flask import Flask, request, jsonify, send_from_directory
import edge_tts
import asyncio
import os
import uuid

app = Flask(__name__)

AUDIO_DIR = os.path.join(os.getcwd(), "audio_files")
os.makedirs(AUDIO_DIR, exist_ok=True)

@app.route("/")
def index():
    return send_from_directory("frontend", "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("frontend", path)

@app.route("/speak", methods=["POST"])
def speak():
    data = request.get_json()
    text = data.get("text", "")
    voice = data.get("voice", "fr-FR-DeniseNeural")

    if not text.strip():
        return jsonify({"error": "Aucun texte reçu"}), 400

    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(AUDIO_DIR, filename)

    try:
        asyncio.run(generate_audio(text, voice, filepath))
        return jsonify({"audio": filename})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

async def generate_audio(text, voice, filepath):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(filepath)

@app.route("/audio/<path:filename>")
def get_audio(filename):
    return send_from_directory(AUDIO_DIR, filename)

if __name__ == "__main__":
    app.run(debug=True)
