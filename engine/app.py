from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from io import BytesIO
import requests
import time

app = Flask(__name__)
CORS(app)

# URLs internas para Docker Compose
FACE_DETECT_URL = "http://bd:5002/detect"
AGE_CLASSIFY_URL = "http://clasit:5003/classify"
PIXELATE_URL = "http://pixelado:5004/pixelate"

# --- SIMULACIÓN TEMPORAL ---
@app.route("/start", methods=["POST"])
def start_pipeline():
    # Simulación: devolver una imagen de prueba mientras no existe la cadena real
    test_image_path = "sample_output.jpg"
    return send_file(test_image_path, mimetype='image/jpeg')


'''
# --- VERSIÓN FUNCIONAL (descomentar cuando tengas todos los microservicios listos) ---
@app.route("/start", methods=["POST"])
def start_pipeline():
    if 'file' not in request.files:
        return jsonify({"error": "No se envió ninguna imagen"}), 400

    file = request.files['file']
    files = {'file': (file.filename, file.read(), file.content_type)}

    # --- Paso 1: detección de rostros ---
    start_detect = time.time()
    face_response = requests.post(FACE_DETECT_URL, files=files)
    end_detect = time.time()

    if face_response.status_code != 200:
        return jsonify({"error": "Error en detección de rostros"}), 500

    print(f"🧠 Tiempo detección de caras: {end_detect - start_detect:.2f}s")

    # --- Paso 2: clasificación de edad ---
    face_data = {'file': ('rostros_detectados.jpg', face_response.content, 'image/jpeg')}
    start_classify = time.time()
    age_response = requests.post(AGE_CLASSIFY_URL, files=face_data)
    end_classify = time.time()

    if age_response.status_code != 200:
        return jsonify({"error": "Error en clasificación de edad"}), 500

    print(f"📊 Tiempo clasificación de edad: {end_classify - start_classify:.2f}s")

    # --- Paso 3: pixelado ---
    age_data = {'file': ('edades.json', age_response.content, 'application/json')}
    start_pixel = time.time()
    pixel_response = requests.post(PIXELATE_URL, files=age_data)
    end_pixel = time.time()

    if pixel_response.status_code != 200:
        return jsonify({"error": "Error en pixelado"}), 500

    print(f"🖼️ Tiempo pixelado: {end_pixel - start_pixel:.2f}s")

    return pixel_response.content, 200, {'Content-Type': 'image/jpeg'}
'''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
