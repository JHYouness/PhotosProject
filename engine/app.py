from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import time
import json  # 👈 necesario para convertir el JSON

app = Flask(__name__)
CORS(app)

# URLs internas
FACE_DETECT_URL = "http://bd:5002/detect"
CLASIFY_URL = "http://clasit:5003/classify"
PIXELATE_URL = "http://pixelado:5004/pixelate"

@app.route("/start", methods=["POST"])
def start_pipeline():
    if 'file' not in request.files:
        return jsonify({"error": "No se envió ninguna imagen"}), 400

    file = request.files['file']
    files = {'file': (file.filename, file.read(), file.content_type)}

    # Paso 1: detección de rostros
    start_detect = time.time()
    face_response = requests.post(FACE_DETECT_URL, files=files)
    end_detect = time.time()
    if face_response.status_code != 200:
        return jsonify({"error": "Error en detección de rostros"}), 500
    print(f"🧠 Tiempo detección de caras: {end_detect - start_detect:.2f}s")

    # Paso 2: clasificación de edad directamente (reemplaza relay)
    face_json = face_response.json()
    payload = {
        'faces_detected': len(face_json.get('faces', [])),
        'faces': face_json.get('faces', [])
    }

    start_classify = time.time()
    age_response = requests.post(CLASIFY_URL, json=payload)
    end_classify = time.time()
    if age_response.status_code != 200:
        return jsonify({"error": "Error en clasificación de edad"}), 500
    print(f"📊 Tiempo clasificación de edad: {end_classify - start_classify:.2f}s")

    # Paso 3: pixelado con imagen + JSON de edades
    file.stream.seek(0)
    image_data = {
        'file': (file.filename, file.read(), file.content_type),
        'ages': ('edades.json',
                 bytes(json.dumps(age_response.json()), encoding='utf-8'),  # ✅ JSON real
                 'application/json')
    }

    start_pixel = time.time()
    pixel_response = requests.post(PIXELATE_URL, files=image_data)
    end_pixel = time.time()
    if pixel_response.status_code != 200:
        return jsonify({"error": "Error en pixelado"}), 500
    print(f"🖼️ Tiempo pixelado: {end_pixel - start_pixel:.2f}s")

    return pixel_response.content, 200, {'Content-Type': 'image/jpeg'}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
