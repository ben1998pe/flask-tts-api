from flask import Flask, request, jsonify, send_file
from gtts import gTTS
import os
import uuid
import time

app = Flask(__name__)
AUDIO_FOLDER = "audios"
MAX_AUDIO_AGE_SECONDS = 60 * 60  # 1 hora

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
        os.makedirs(AUDIO_FOLDER, exist_ok=True)
        limpiar_audios_antiguos()

        tts = gTTS(text=texto, lang=idioma)
        filename = f"{uuid.uuid4()}.mp3"
        filepath = os.path.join(AUDIO_FOLDER, filename)
        tts.save(filepath)

        return send_file(filepath, mimetype="audio/mpeg", as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def limpiar_audios_antiguos():
    now = time.time()
    for archivo in os.listdir(AUDIO_FOLDER):
        ruta = os.path.join(AUDIO_FOLDER, archivo)
        if os.path.isfile(ruta):
            edad = now - os.path.getmtime(ruta)
            if edad > MAX_AUDIO_AGE_SECONDS:
                os.remove(ruta)

if __name__ == "__main__":
    app.run(debug=True)
