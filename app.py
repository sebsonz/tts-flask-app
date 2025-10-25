from flask import Flask, request, jsonify, send_from_directory
from gtts import gTTS
import os
import uuid
import json
from datetime import datetime

app = Flask(__name__, static_folder="frontend", template_folder="frontend")

# Dossiers
AUDIO_DIR = os.path.join(os.getcwd(), "audio_files")
os.makedirs(AUDIO_DIR, exist_ok=True)

# Fichier historique
HISTORY_FILE = os.path.join(AUDIO_DIR, "history.json")
if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


# Serve static frontend files (css, js)
@app.route("/<path:filename>")
def frontend_files(filename):
    return send_from_directory(app.static_folder, filename)


@app.route("/health")
def health():
    return "OK", 200


@app.route("/tts", methods=["POST"])
def tts():
    try:
        data = request.get_json() or {}
        text = data.get("text", "").strip()
        lang = data.get("lang", "fr")
        # speed and voice_gender are handled client-side (playbackRate)
        if not text:
            return jsonify({"error": "Aucun texte reçu"}), 400

        # Générer nom de fichier unique
        filename = f"{uuid.uuid4().hex}.mp3"
        filepath = os.path.join(AUDIO_DIR, filename)

        # Génération gTTS (écrit dans audio_files)
        tts_obj = gTTS(text=text, lang=lang, tld="com")
        tts_obj.save(filepath)

        # Enregistrer l'entrée d'historique
        entry = {
            "id": uuid.uuid4().hex,
            "filename": filename,
            "audio_url": f"/audio/{filename}",
            "text": text,
            "lang": lang,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        with open(HISTORY_FILE, "r+", encoding="utf-8") as f:
            try:
                history = json.load(f)
            except Exception:
                history = []
            history.append(entry)
            # garder seulement dernières 50 entrées
            history = history[-50:]
            f.seek(0)
            f.truncate(0)
            json.dump(history, f, ensure_ascii=False, indent=2)

        return jsonify(entry)
    except Exception as e:
        # log server-side (Render logs)
        print("TTS ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/audio/<path:filename>")
def serve_audio(filename):
    # Sert les fichiers générés dans audio_files
    return send_from_directory(AUDIO_DIR, filename, mimetype="audio/mpeg")


@app.route("/history", methods=["GET"])
def get_history():
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
        # retourner en ordre inverse (plus récent en premier)
        return jsonify(list(reversed(history)))
    except Exception:
        return jsonify([])


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
