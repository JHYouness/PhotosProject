from flask import Flask, request, jsonify
from retinaface import RetinaFace
import cv2
import numpy as np
import base64

app = Flask(__name__)

@app.route('/detect', methods=['POST'])
def detect_faces():
    if 'file' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['file']
    image_bytes = file.read()
    npimg = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    if img is None:
        return jsonify({'error': 'No se pudo decodificar la imagen'}), 400

    detections = RetinaFace.detect_faces(img)

    face_data_list = []
    for key in detections:
        face = detections[key]
        x1, y1, x2, y2 = face["facial_area"]

        # Recortar la cara
        cropped_face = img[y1:y2, x1:x2]

        # Codificar en base64
        _, cropped_encoded = cv2.imencode('.jpg', cropped_face)
        cropped_base64 = base64.b64encode(cropped_encoded).decode('utf-8')

        face_data_list.append({
            'x1': int(x1),
            'y1': int(y1),
            'x2': int(x2),
            'y2': int(y2),
            'face_image': cropped_base64
        })

    return jsonify({'faces': face_data_list})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
