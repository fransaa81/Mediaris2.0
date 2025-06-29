import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Obtiene la ruta del directorio donde se encuentra app.py y construye la ruta completa hacia "api_key"
script_dir = os.path.dirname(os.path.realpath(__file__))
api_key_path = os.path.join(script_dir, "api_key")

with open(api_key_path, "r") as key_file:
    API_KEY = key_file.read().strip()

# Configuración del asistent
ASSISTANT_ID = "asst_9kQZSR2x7Gi2OjjxlPwMsdN2"
OPENAI_ASSISTANT_URL = "https://platform.openai.com/playground/assistants"

@app.route('/start_assistant', methods=['POST'])
def start_assistant():
    # Recibe datos enviados desde el frontend
    data = request.get_json()
    user_name = data.get('userName', '')
    user_topic = data.get('userTopic', '')
    
    # Construye el payload para el assistant
    payload = {
        "assistant_id": ASSISTANT_ID,
        "user_name": user_name,
        "user_topic": user_topic,
        "message": "Conectando con el asistent..."
    }
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(OPENAI_ASSISTANT_URL, json=payload, headers=headers)
        response.raise_for_status()  # Lanza error si la respuesta no es 200
        print("Respuesta sin parsear:", response.text)
        try:
            result = response.json()
        except ValueError:
            return jsonify({
                "status": "error",
                "message": "Respuesta JSON inválida: " + response.text
            }), 500
        return jsonify({"status": "success", "data": result}), 200
    except requests.RequestException as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)