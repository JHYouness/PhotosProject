from flask import Flask, request, send_file, jsonify
import cv2
import numpy as np
from io import BytesIO

app = Flask(__name__)

# Cargar clasificador de caras de OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

@app.route('/detect', methods=['POST'])
def detect_faces():
    if 'file' not in request.files:
        return jsonify({"error": "No se envió imagen"}), 400

    file = request.files['file']
    npimg = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # Convertir a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detectar caras
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Dibujar rectángulos
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Codificar imagen para enviar
    _, img_encoded = cv2.imencode('.jpg', img)
    return send_file(BytesIO(img_encoded.tobytes()), mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
