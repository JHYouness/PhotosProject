from flask import Flask, request, jsonify
import base64
import numpy as np
import cv2
import tensorflow as tf

app = Flask(__name__)

# Cargar el modelo una sola vez al inicio
model = tf.keras.models.load_model("modelo_edad.keras")

# Función para convertir base64 a imagen
def decode_base64_image(b64_string):
    try:
        decoded = base64.b64decode(b64_string)
        img_array = np.frombuffer(decoded, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        return img
    except Exception as e:
        print("[ERROR] Fallo al decodificar imagen:", e, flush=True)
        return None

# Preprocesamiento según lo que tu modelo espere
def preprocess_image(img):
    resized = cv2.resize(img, (224, 224))  # ajusta si tu modelo usa otra forma
    normalized = resized / 255.0
    return np.expand_dims(normalized, axis=0)

@app.route('/classify', methods=['POST'])
def classify_age():
    data = request.get_json()
    if not data or 'faces' not in data:
        return jsonify({"error": "No se enviaron caras"}), 400

    results = []
    for face in data['faces']:
        img = decode_base64_image(face['face_image'])
        if img is None:
            continue

        processed = preprocess_image(img)

        try:
            prediction = model.predict(processed)
            pred_value = prediction[0][0]
            print("==== DEBUG CLASIT ====")
            print(f"Resultado bruto del modelo: {prediction}")
            print(f"Valor final: {pred_value}", flush=True)
        except Exception as e:
            print("[ERROR] Fallo al predecir:", e, flush=True)
            pred_value = 0.0

        # 🧪 Forzado temporal: pixelar siempre
        es_menor = True
        # es_menor = pred_value < 0.5  ← esto lo usarás cuando el modelo esté bien

        results.append({
            "es_menor": es_menor,
            "confianza": 1.0,
            "box": [face["x1"], face["y1"], face["x2"] - face["x1"], face["y2"] - face["y1"]]
        })

    return jsonify(results), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
