from flask import Flask, request, send_file, jsonify
import cv2
import numpy as np
from io import BytesIO

app = Flask(__name__)

@app.route('/pixelate', methods=['POST'])
def pixelate_faces():
    if 'file' not in request.files:
        return jsonify({"error": "No se envió imagen"}), 400

    file = request.files['file']
    npimg = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # Simulación: pixelar una región fija de la imagen
    x, y, w, h = 50, 50, 100, 100
    face = img[y:y+h, x:x+w]
    face = cv2.resize(face, (10, 10), interpolation=cv2.INTER_LINEAR)
    face = cv2.resize(face, (w, h), interpolation=cv2.INTER_NEAREST)
    img[y:y+h, x:x+w] = face

    # Codificar imagen para devolverla como respuesta
    _, img_encoded = cv2.imencode('.jpg', img)
    return send_file(BytesIO(img_encoded.tobytes()), mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
