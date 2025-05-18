from flask import Flask, request, jsonify, send_file
from gtts import gTTS
import os
import uuid

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"mensaje": "Bienvenido a la API de texto a voz con gTTS 🚀"})

@app.route("/tts", methods=["POST"])
def texto_a_voz():
    data = request.get_json()

    if not data or "texto" not in data:
        return jsonify({"error": "Debes enviar un campo 'texto' en el JSON."}), 400

    texto = data["texto"]
    idioma = data.get("idioma", "es")

    try:
        tts = gTTS(text=texto, lang=idioma)
        filename = f"{uuid.uuid4()}.mp3"
        filepath = os.path.join("audios", filename)

        os.makedirs("audios", exist_ok=True)
        tts.save(filepath)

        return send_file(filepath, mimetype="audio/mpeg", as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
