from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# URLs internas (ajustadas en docker-compose con nombres de servicio)
FACE_DETECT_URL = "http://bd/detect"
AGE_CLASSIFY_URL = "http://clasit/classify"
PIXELATE_URL = "http://pixelado/pixelate"

@app.route("/start", methods=["POST"])
def start_pipeline():
    if 'file' not in request.files:
        return jsonify({"error": "No se envió ninguna imagen"}), 400

    file = request.files['file']
    files = {'file': (file.filename, file.read(), file.content_type)}

    # Paso 1: detección de rostros
    face_response = requests.post(FACE_DETECT_URL, files=files)
    if face_response.status_code != 200:
        return jsonify({"error": "Error en detección de rostros"}), 500

    # Paso 2: clasificación de edad
    face_data = {'file': ('rostros_detectados.jpg', face_response.content, 'image/jpeg')}
    age_response = requests.post(AGE_CLASSIFY_URL, files=face_data)
    if age_response.status_code != 200:
        return jsonify({"error": "Error en clasificación de edad"}), 500

    # Paso 3: pixelado
    age_data = {'file': ('edades.json', age_response.content, 'application/json')}
    pixel_response = requests.post(PIXELATE_URL, files=age_data)

    if pixel_response.status_code != 200:
        return jsonify({"error": "Error en pixelado"}), 500

    return pixel_response.content, 200, {'Content-Type': 'image/jpeg'}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
