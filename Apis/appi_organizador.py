from flask import Flask, request, jsonify, send_file
import uuid
import os
import requests
from io import BytesIO

app = Flask(__name__)

# Simulación de almacenamiento en memoria (usar base de datos real en producción)
procesos = {}

# Configura URLs reales en producción
API_C_URL = "http://api-c.com/procesar"
API_D_URL = "http://api-d.com/procesar"
API_E_URL = "http://api-e.com/procesar"
API_A_CALLBACK = "http://api-a.com/callback-final"

@app.route("/start", methods=["POST"])
def start_proceso():
    if 'file' not in request.files:
        return jsonify({"error": "Falta archivo"}), 400

    file = request.files['file']
    proceso_id = str(uuid.uuid4())
    procesos[proceso_id] = {'etapa': 'inicio'}

    # Enviar a API C
    files = {'file': (file.filename, file.read(), file.content_type)}
    data = {'proceso_id': proceso_id}
    requests.post(API_C_URL, files=files, data=data)

    return jsonify({"proceso_id": proceso_id, "estado": "enviado a C"}), 200


@app.route("/callback/c", methods=["POST"])
def callback_c():
    proceso_id = request.form.get("proceso_id")
    file = request.files['file']

    procesos[proceso_id]['etapa'] = 'recibido de C'

    # Enviar a API D
    files = {'file': (file.filename, file.read(), file.content_type)}
    data = {'proceso_id': proceso_id}
    requests.post(API_D_URL, files=files, data=data)

    return '', 200


@app.route("/callback/d", methods=["POST"])
def callback_d():
    proceso_id = request.form.get("proceso_id")
    file = request.files['file']

    procesos[proceso_id]['etapa'] = 'recibido de D'

    # Enviar a API E
    files = {'file': (file.filename, file.read(), file.content_type)}
    data = {'proceso_id': proceso_id}
    requests.post(API_E_URL, files=files, data=data)

    return '', 200


@app.route("/callback/e", methods=["POST"])
def callback_e():
    proceso_id = request.form.get("proceso_id")
    file = request.files['file']
    procesos[proceso_id]['etapa'] = 'recibido de E'

    # Enviar resultado final a API A
    files = {'file': (file.filename, file.read(), file.content_type)}
    data = {'proceso_id': proceso_id}
    requests.post(API_A_CALLBACK, files=files, data=data)

    procesos[proceso_id]['etapa'] = 'completado'
    return '', 200

if __name__ == "__main__":
    app.run(debug=True)
