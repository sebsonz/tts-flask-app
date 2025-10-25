from flask import Flask, request, jsonify, send_from_directory
import os
import uuid

app = Flask(__name__)

# ✅ Assure que le dossier audio existe
AUDIO_FOLDER = "audio_files"
os.makedirs(AUDIO_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return "Application TTS prête 🚀"


# ✅ Route pour générer l’audio
@app.route("/api/tts", methods=["POST"])
def text_to_speech():
    data = request.get_json()
    text = data.get("text", "")

    if not text.strip():
        return jsonify({"error": "Text is empty"}), 400

    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(AUDIO_FOLDER, filename)

    # ✅ Exemple : écriture d’un faux son temporaire (à remplacer par vrai TTS)
    with open(filepath, "wb") as f:
        f.write(b"FAKE_MP3_DATA")

    return jsonify({"url": f"/audio/{filename}"})


# ✅ Route pour servir les fichiers audio au navigateur
@app.route("/audio/<filename>")
def serve_audio(filename):
    return send_from_directory(AUDIO_FOLDER, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
