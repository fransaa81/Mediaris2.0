from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import time
import requests
from dotenv import load_dotenv

# Construir la ruta absoluta del archivo de entorno
env_path = os.path.join(os.path.dirname(__file__), 'api_key.env')
print("Cargando variables de entorno desde:", env_path)

# Cargar el archivo de entorno
load_dotenv(env_path)

# Verifica que la API key se cargue correctamente
API_KEY = os.getenv('API_KEY')
print("API_KEY:", API_KEY)

app = Flask(__name__)
CORS(app)  # Permite requests desde el frontend

# --- Verificación de conexión con OpenAI ---
def verify_openai_connection():
    try:
        print("Verificando conexión con OpenAI...")
        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        }
        
        # Test simple para verificar la API key
        response = requests.get(
            'https://api.openai.com/v1/models',
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Conexión con OpenAI verificada correctamente")
            return True
        else:
            print(f"❌ Error de conexión: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error al verificar conexión: {e}")
        return False

# Verificar conexión al iniciar
openai_available = verify_openai_connection()

ASSISTANT_ID = "asst_9kQZSR2x7Gi2OjjxlPwMsdN2"

# Variable global para mantener el thread activo
current_thread_id = None

@app.route('/start_assistant', methods=['POST'])
def start_assistant():
    global current_thread_id
    print("=== INICIO DE start_assistant ===")
    print("Recibida solicitud en /start_assistant")
    
    if not openai_available or not API_KEY:
        error_msg = "El cliente de OpenAI no está disponible. Revisa el archivo api_key.env"
        print(f"ERROR: {error_msg}")
        return jsonify({"status": "error", "message": error_msg}), 500

    try:
        data = request.get_json()
        print(f"Datos recibidos: {data}")
        
        user_name = data.get('userName', 'Usuario')
        user_topic = data.get('userTopic', 'consulta general')
        
        initial_message = f"Hola, mi nombre es {user_name}. El tema sobre el que quiero conversar es: {user_topic}."
        print(f"Mensaje inicial: {initial_message}")

        # Crear nuevo thread usando requests
        print("Creando thread...")
        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json',
            'OpenAI-Beta': 'assistants=v2'
        }
        
        response = requests.post(
            'https://api.openai.com/v1/threads',
            headers=headers,
            json={}
        )
        
        print(f"Respuesta crear thread - Status: {response.status_code}")
        print(f"Respuesta crear thread - Text: {response.text}")
        
        if response.status_code != 200:
            raise Exception(f"Error creando thread: {response.text}")
            
        thread_data = response.json()
        current_thread_id = thread_data['id']
        print(f"Thread creado: {current_thread_id}")

        # Añadir mensaje inicial
        print("Añadiendo mensaje al thread...")
        response = requests.post(
            f'https://api.openai.com/v1/threads/{current_thread_id}/messages',
            headers=headers,
            json={
                'role': 'user',
                'content': initial_message
            }
        )
        
        print(f"Respuesta añadir mensaje - Status: {response.status_code}")
        print(f"Respuesta añadir mensaje - Text: {response.text}")
        
        if response.status_code != 200:
            raise Exception(f"Error añadiendo mensaje: {response.text}")

        # Ejecutar asistente
        print(f"Ejecutando asistente con ID: {ASSISTANT_ID}")
        response = requests.post(
            f'https://api.openai.com/v1/threads/{current_thread_id}/runs',
            headers=headers,
            json={
                'assistant_id': ASSISTANT_ID
            }
        )
        
        print(f"Respuesta ejecutar asistente - Status: {response.status_code}")
        print(f"Respuesta ejecutar asistente - Text: {response.text}")
        
        if response.status_code != 200:
            raise Exception(f"Error ejecutando asistente: {response.text}")
            
        run_data = response.json()
        run_id = run_data['id']
        print(f"Run creado: {run_id}, estado: {run_data['status']}")

        # Esperar respuesta
        max_attempts = 30
        attempts = 0
        
        while attempts < max_attempts:
            print(f"Esperando... intento: {attempts + 1}")
            time.sleep(1)
            
            response = requests.get(
                f'https://api.openai.com/v1/threads/{current_thread_id}/runs/{run_id}',
                headers=headers
            )
            
            if response.status_code != 200:
                raise Exception(f"Error obteniendo estado del run: {response.text}")
                
            run_data = response.json()
            status = run_data['status']
            
            if status not in ['queued', 'in_progress']:
                break
                
            attempts += 1

        print(f"Estado final del run: {status}")

        if status == 'completed':
            print("Obteniendo respuesta...")
            response = requests.get(
                f'https://api.openai.com/v1/threads/{current_thread_id}/messages',
                headers=headers
            )
            
            if response.status_code != 200:
                raise Exception(f"Error obteniendo mensajes: {response.text}")
                
            messages_data = response.json()
            assistant_response = messages_data['data'][0]['content'][0]['text']['value']
            print(f"Respuesta del asistente: {assistant_response[:100]}...")
            
            return jsonify({
                "status": "success",
                "data": {
                    "response": assistant_response
                }
            }), 200
        else:
            error_msg = f"La ejecución del asistente falló con el estado: {status}"
            print(f"ERROR: {error_msg}")
            # Si hay más detalles del error, agregarlos
            if 'last_error' in run_data and run_data['last_error']:
                error_msg += f" - Detalle: {run_data['last_error']}"
            return jsonify({"status": "error", "message": error_msg}), 500

    except Exception as e:
        error_msg = f"Error en la API de OpenAI: {str(e)}"
        print(f"EXCEPCIÓN: {error_msg}")
        import traceback
        print(f"TRACEBACK: {traceback.format_exc()}")
        return jsonify({"status": "error", "message": error_msg}), 500

@app.route('/send_message', methods=['POST'])
def send_message():
    global current_thread_id
    print("Recibida solicitud en /send_message")
    
    if not openai_available or not current_thread_id:
        return jsonify({"status": "error", "message": "No hay conversación activa"}), 500

    try:
        data = request.get_json()
        message = data.get('message', '')
        print(f"Mensaje recibido: {message}")

        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json',
            'OpenAI-Beta': 'assistants=v2'
        }

        # Añadir mensaje del usuario
        response = requests.post(
            f'https://api.openai.com/v1/threads/{current_thread_id}/messages',
            headers=headers,
            json={
                'role': 'user',
                'content': message
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"Error añadiendo mensaje: {response.text}")

        # Ejecutar asistente
        response = requests.post(
            f'https://api.openai.com/v1/threads/{current_thread_id}/runs',
            headers=headers,
            json={
                'assistant_id': ASSISTANT_ID
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"Error ejecutando asistente: {response.text}")
            
        run_data = response.json()
        run_id = run_data['id']

        # Esperar respuesta
        max_attempts = 30
        attempts = 0
        
        while attempts < max_attempts:
            time.sleep(1)
            
            response = requests.get(
                f'https://api.openai.com/v1/threads/{current_thread_id}/runs/{run_id}',
                headers=headers
            )
            
            if response.status_code != 200:
                raise Exception(f"Error obteniendo estado del run: {response.text}")
                
            run_data = response.json()
            status = run_data['status']
            
            if status not in ['queued', 'in_progress']:
                break
                
            attempts += 1

        if status == 'completed':
            response = requests.get(
                f'https://api.openai.com/v1/threads/{current_thread_id}/messages',
                headers=headers
            )
            
            if response.status_code != 200:
                raise Exception(f"Error obteniendo mensajes: {response.text}")
                
            messages_data = response.json()
            assistant_response = messages_data['data'][0]['content'][0]['text']['value']
            
            return jsonify({
                "status": "success",
                "data": {
                    "response": assistant_response
                }
            }), 200
        else:
            return jsonify({"status": "error", "message": f"Error en la ejecución: {status}"}), 500

    except Exception as e:
        print(f"Error en send_message: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "Backend funcionando correctamente"}), 200

if __name__ == '__main__':
    print("Iniciando servidor Flask...")
    app.run(debug=True, host='127.0.0.1', port=5000)