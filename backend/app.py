from flask import Flask, request, jsonify
from openai import OpenAI
from flask_cors import CORS
import os
import time
from dotenv import load_dotenv

# Construir la ruta absoluta del archivo de entorno
env_path = os.path.join(os.path.dirname(__file__), 'api_key.env')
print("Cargando variables de entorno desde:", env_path)

# Cargar el archivo de entorno
load_dotenv(env_path)

# Verifica que la API key se cargue correctamente
api_key = os.getenv('API_KEY')
print("API_KEY:", api_key)

app = Flask(__name__)
CORS(app)  # Permite requests desde el frontend

# --- Inicialización del cliente de OpenAI ---
try:
    API_KEY = os.getenv('API_KEY')
    if not API_KEY:
        raise Exception("La variable de entorno API_KEY no está definida")
    client = OpenAI(api_key=API_KEY)
    print("Cliente de OpenAI inicializado correctamente")
except Exception as e:
    print(f"ERROR al inicializar OpenAI: {e}")
    API_KEY = None
    client = None

ASSISTANT_ID = "asst_9kQZSR2x7Gi2OjjxlPwMsdN2"

# Variable global para mantener el thread activo
current_thread_id = None

@app.route('/start_assistant', methods=['POST'])
def start_assistant():
    global current_thread_id
    print("Recibida solicitud en /start_assistant")
    
    if not client:
        error_msg = "El cliente de OpenAI no está inicializado. Revisa el archivo api_key."
        print(f"ERROR: {error_msg}")
        return jsonify({"status": "error", "message": error_msg}), 500

    try:
        data = request.get_json()
        print(f"Datos recibidos: {data}")
        
        user_name = data.get('userName', '')
        user_topic = data.get('userTopic', '')
        
        initial_message = f"Hola, mi nombre es {user_name}. El tema sobre el que quiero conversar es: {user_topic}."
        print(f"Mensaje inicial: {initial_message}")

        # Crear nuevo thread
        print("Creando thread...")
        thread = client.beta.threads.create()
        current_thread_id = thread.id  # Guardar el thread ID
        print(f"Thread creado: {thread.id}")

        # Añadir mensaje inicial
        print("Añadiendo mensaje al thread...")
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=initial_message
        )

        # Ejecutar asistente
        print("Ejecutando asistente...")
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID,
        )
        print(f"Run creado: {run.id}, estado: {run.status}")

        # Esperar respuesta
        max_attempts = 30
        attempts = 0
        
        while run.status in ['queued', 'in_progress'] and attempts < max_attempts:
            print(f"Esperando... Estado: {run.status}, intento: {attempts + 1}")
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            attempts += 1

        print(f"Estado final del run: {run.status}")

        if run.status == 'completed':
            print("Obteniendo respuesta...")
            messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )
            assistant_response = messages.data[0].content[0].text.value
            print(f"Respuesta del asistente: {assistant_response[:100]}...")
            
            return jsonify({
                "status": "success",
                "data": {
                    "response": assistant_response
                }
            }), 200
        else:
            error_msg = f"La ejecución del asistente falló con el estado: {run.status}"
            print(f"ERROR: {error_msg}")
            return jsonify({"status": "error", "message": error_msg}), 500

    except Exception as e:
        error_msg = f"Error en la API de OpenAI: {str(e)}"
        print(f"EXCEPCIÓN: {error_msg}")
        return jsonify({"status": "error", "message": error_msg}), 500

@app.route('/send_message', methods=['POST'])
def send_message():
    global current_thread_id
    print("Recibida solicitud en /send_message")
    
    if not client or not current_thread_id:
        return jsonify({"status": "error", "message": "No hay conversación activa"}), 500

    try:
        data = request.get_json()
        message = data.get('message', '')
        print(f"Mensaje recibido: {message}")

        # Añadir mensaje del usuario
        client.beta.threads.messages.create(
            thread_id=current_thread_id,
            role="user",
            content=message
        )

        # Ejecutar asistente
        run = client.beta.threads.runs.create(
            thread_id=current_thread_id,
            assistant_id=ASSISTANT_ID,
        )

        # Esperar respuesta
        max_attempts = 30
        attempts = 0
        
        while run.status in ['queued', 'in_progress'] and attempts < max_attempts:
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=current_thread_id,
                run_id=run.id
            )
            attempts += 1

        if run.status == 'completed':
            messages = client.beta.threads.messages.list(
                thread_id=current_thread_id
            )
            assistant_response = messages.data[0].content[0].text.value
            
            return jsonify({
                "status": "success",
                "data": {
                    "response": assistant_response
                }
            }), 200
        else:
            return jsonify({"status": "error", "message": f"Error en la ejecución: {run.status}"}), 500

    except Exception as e:
        print(f"Error en send_message: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "Backend funcionando correctamente"}), 200

if __name__ == '__main__':
    print("Iniciando servidor Flask...")
    app.run(debug=True, host='127.0.0.1', port=5000)