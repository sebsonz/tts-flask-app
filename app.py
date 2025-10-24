from flask import Flask, request, render_template, send_file, jsonify
from gtts import gTTS
from io import BytesIO
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/speak", methods=["POST"])
def speak():
    try:
        data = request.get_json()
        text = data.get("text", "").strip()

        if not text:
            return jsonify({"error": "No text provided"}), 400

        tts = gTTS(text=text, lang="fr")

        audio_data = BytesIO()
        tts.write_to_fp(audio_data)
        audio_data.seek(0)

        return send_file(
            audio_data,
            mimetype="audio/mp3",
            as_attachment=False
        )
    
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Audio generation failed"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
