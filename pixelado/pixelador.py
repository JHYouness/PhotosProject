from flask import Flask, request, send_file, jsonify
import cv2
import numpy as np
import base64
import json
from io import BytesIO

app = Flask(__name__)

@app.route('/pixelate', methods=['POST'])
def pixelate_faces():
    if 'file' not in request.files:
        return jsonify({"error": "No se envió imagen"}), 400

    file = request.files['file']
    npimg = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    if img is None:
        return jsonify({'error': 'No se pudo decodificar la imagen.'}), 500

    if 'ages' not in request.files:
        return jsonify({'error': 'No se enviaron datos de edad'}), 400

    # Leer JSON con edades y coordenadas
    age_json = request.files['ages'].read().decode('utf-8')
    age_data = json.loads(age_json)

    for face in age_data:
        if face.get("es_menor", False):
            x, y, w, h = face["box"]
            x, y, w, h = int(x), int(y), int(w), int(h)

            # Pixelar rostro
            face_region = img[y:y+h, x:x+w]
            if face_region.size == 0:
                continue  # evitar errores si los datos son inválidos
            face_region = cv2.resize(face_region, (10, 10), interpolation=cv2.INTER_LINEAR)
            face_region = cv2.resize(face_region, (w, h), interpolation=cv2.INTER_NEAREST)
            img[y:y+h, x:x+w] = face_region

    # Codificar resultado
    _, img_encoded = cv2.imencode('.jpg', img)
    return send_file(BytesIO(img_encoded.tobytes()), mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
