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
