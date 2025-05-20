from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Almacén en memoria para rostros recibidos
received_faces = []

@app.route('/api/receive_faces', methods=['POST'])
def receive_faces():
    global received_faces
    received_faces.clear()

    data = request.get_json()

    if 'faces' not in data:
        return jsonify({'error': 'No se han proporcionado los datos necesarios'}), 404

    for i, face in enumerate(data['faces']):
        coords = {
            'x1': face['x1'],
            'y1': face['y1'],
            'x2': face['x2'],
            'y2': face['y2']
        }

        # Comprobación básica
        face_image_b64 = face.get('face_image')
        if not face_image_b64:
            return jsonify({'error': 'No se han proporcionado las caras'}), 404

        # Almacenar en memoria
        received_faces.append({
            'coordinates': coords,
            'face_image': face_image_b64
        })

    payload = {
        'faces_detected': len(received_faces),
        'faces': received_faces
    }

    response = requests.post("http://localhost:7000/api/model_predict_ages", json=payload)
    return jsonify({'status': 'enviado', 'response': response.json()})

if __name__ == '__main__':
    app.run(port=6000, debug=True)
