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

    print("📌 TEXTE REÇU :", text)

    if not text:
        print("❌ Aucun texte reçu !")
        return jsonify({"error": "No text provided"}), 400

    try:
        filename = f"{uuid.uuid4()}.mp3"
        filepath = os.path.join("/tmp", filename)

        print("📌 Emplacement temporaire :", filepath)

        # Génération TTS
        tts = gTTS(text=text, lang="fr")
        tts.save(filepath)

        # ✅ Vérifier si le fichier a été généré
        exists = os.path.exists(filepath)
        size = os.path.getsize(filepath) if exists else 0

        print("📦 Fichier existant :", exists)
        print("🔍 Taille en octets :", size)

        if not exists or size == 0:
            print("❌ Le fichier audio est vide !")
            return jsonify({"error": "Audio generation failed"}), 500

        print("✅ Envoi du fichier au client")

        return send_file(filepath, mimetype="audio/mpeg")
    except Exception as e:
        print("⚠️ Erreur :", str(e))
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
