from flask import Flask, request, send_file, jsonify, render_template
from gtts import gTTS
import os
import uuid

app = Flask(__name__, static_folder="frontend", template_folder="frontend")

# ✅ Route principale : interface web
@app.route('/')
def home():
    return app.send_static_file('index.html')

# ✅ Route de santé pour éviter la mise en veille Render
@app.route('/health')
def health():
    return "OK", 200

# ✅ Route TTS : génération audio
@app.route('/speak', methods=['POST'])
def speak():
    data = request.json or {}
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        # Render n'autorise l'écriture que dans /tmp
        filename = f"{uuid.uuid4()}.mp3"
        filepath = os.path.join("/tmp", filename)

        # gTTS pour générer l’audio
        tts = gTTS(text=text, lang="fr")
        tts.save(filepath)

        return send_file(filepath, mimetype="audio/mpeg")
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
