from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route('/classify', methods=['POST'])
def classify_age():
    if 'file' not in request.files:
        return jsonify({"error": "No se envió imagen"}), 400

    # Simulación: devolver edad aleatoria
    edad = random.randint(12, 30)
    resultado = {
        "edad": edad,
        "es_menor": edad < 18
    }

    return jsonify(resultado), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
