from flask import Flask, request, jsonify
from retinaface import RetinaFace
import cv2
import numpy as np
import base64
import requests

app = Flask(__name__)

@app.route('/detect', methods=['POST'])
def detect_faces():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    image_bytes = file.read()
    npimg = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    temp_path = 'temp.jpg'
    cv2.imwrite(temp_path, img)

    detections = RetinaFace.detect_faces(temp_path)

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

        # Dibujar el rectángulo en la imagen original (opcional)
        cv2.rectangle(img, (x1, y1), (x2, y2), (110, 255, 0), 2)

    # Codificar la imagen original con los recuadros
    _, img_encoded = cv2.imencode('.jpg', img)
    img_base64 = base64.b64encode(img_encoded).decode('utf-8')

    payload = {
        'faces_detected': len(detections),
        'image': img_base64,
        'faces': face_data_list
    }

    # Enviar a otra API (ajusta la URL)
    response = requests.post("http://localhost:5001/receive_faces", json=payload)

    return jsonify({
        'status': 'processed',
        'faces_detected': len(detections),
        'forward_response': response.json()
    })

if __name__ == '__main__':
    app.run(port=5002, debug=True)
