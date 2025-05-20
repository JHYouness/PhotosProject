from flask import Flask, request, jsonify, send_from_directory
import os
import requests
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuración de carpetas
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = os.path.join(UPLOAD_FOLDER, 'processed')
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# Extensiones permitidas
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Dirección del motor engine
ENGINE_URL = 'http://engine:5001/start'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_and_process():
    if 'image' not in request.files:
        return jsonify({'error': 'No se envió ninguna imagen'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Nombre de archivo vacío'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        # Enviar la imagen al engine
        files = {'file': (filename, file.read(), file.content_type)}
        try:
            response = requests.post(ENGINE_URL, files=files)
            if response.status_code != 200:
                return jsonify({'error': 'Fallo al procesar la imagen'}), 500

            # Guardar la imagen procesada
            processed_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
            with open(processed_path, 'wb') as f:
                f.write(response.content)

            return jsonify({'message': 'Procesado correctamente', 'filename': filename}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    else:
        return jsonify({'error': 'Tipo de archivo no permitido'}), 400

# Endpoint para servir imagen procesada
@app.route('/uploads/processed/<filename>')
def serve_processed_image(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
