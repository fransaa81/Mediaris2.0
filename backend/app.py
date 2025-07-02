from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Construir la ruta absoluta del archivo de entorno
env_path = os.path.join(os.path.dirname(__file__), 'api_key.env')
print("Cargando variables de entorno desde:", env_path)

# Cargar el archivo de entorno
load_dotenv(env_path)

# Verifica que la API key se cargue correctamente
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
print("GEMINI_API_KEY:", GEMINI_API_KEY[:20] + "..." if GEMINI_API_KEY else "No encontrada")

# Configurar Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    print("✅ Gemini configurado correctamente")
    gemini_available = True
else:
    print("❌ GEMINI_API_KEY no encontrada en el archivo .env")
    gemini_available = False

app = Flask(__name__)
CORS(app)  # Permite requests desde el frontend

# Sistema de prompt para mediación
MEDIATOR_PROMPT = """Eres un mediador profesional especializado en resolución de conflictos. Tu objetivo es ayudar a las personas a comunicarse mejor y encontrar soluciones.

PASOS PRINCIPALES:
1. Pregunta SOLO el nombre y apellido de la persona (una pregunta a la vez)
2. Después pregunta cuántas personas participarán en esta mediación 
3. Explica brevemente cómo trabajarás
4. Permite que cada parte exprese su perspectiva sin interrupciones
5. Identifica puntos en común y diferencias
6. Guía hacia soluciones constructivas
7. Ayuda a formalizar acuerdos

INSTRUCCIONES IMPORTANTES:
- Haz UNA SOLA pregunta por mensaje, no múltiples preguntas juntas
- Usa siempre el nombre de la persona, nunca digas "usuario"
- Tus preguntas deben ser concisas (máximo 2-3 líneas)
- Tus respuestas pueden ser extensas si es necesario
- Usa un lenguaje empático, neutral y profesional
- Saluda cordialmente y haz UNA pregunta a la vez
- Espera la respuesta antes de continuar con el siguiente paso"""

# Variable global para mantener el historial de conversación
conversation_history = []

@app.route('/start_assistant', methods=['POST'])
def start_assistant():
    global conversation_history
    print("=== INICIO DE start_assistant ===")
    print("Recibida solicitud en /start_assistant")
    
    if not gemini_available:
        error_msg = "Gemini no está disponible. Revisa el archivo api_key.env"
        print(f"ERROR: {error_msg}")
        return jsonify({"status": "error", "message": error_msg}), 500

    try:
        data = request.get_json()
        print(f"Datos recibidos: {data}")
        
        user_name = data.get('userName', 'Usuario')
        user_topic = data.get('userTopic', 'consulta general')
        
        # Reiniciar conversación
        conversation_history = []
        
        initial_message = f"Hola, mi nombre es {user_name}. El tema sobre el que quiero conversar es: {user_topic}."
        print(f"Mensaje inicial: {initial_message}")

        # Crear el prompt completo
        full_prompt = f"{MEDIATOR_PROMPT}\n\nUsuario: {initial_message}"
        
        # Generar respuesta con Gemini
        print("Generando respuesta con Gemini...")
        response = model.generate_content(full_prompt)
        assistant_response = response.text
        
        # Guardar en historial
        conversation_history.append({"role": "user", "content": initial_message})
        conversation_history.append({"role": "assistant", "content": assistant_response})
        
        print(f"Respuesta del mediador: {assistant_response[:100]}...")
        
        return jsonify({
            "status": "success",
            "data": {
                "response": assistant_response
            }
        }), 200

    except Exception as e:
        error_msg = f"Error en Gemini: {str(e)}"
        print(f"EXCEPCIÓN: {error_msg}")
        import traceback
        print(f"TRACEBACK: {traceback.format_exc()}")
        return jsonify({"status": "error", "message": error_msg}), 500

@app.route('/send_message', methods=['POST'])
def send_message():
    global conversation_history
    print("Recibida solicitud en /send_message")
    
    if not gemini_available:
        return jsonify({"status": "error", "message": "Gemini no está disponible"}), 500

    try:
        data = request.get_json()
        message = data.get('message', '')
        print(f"Mensaje recibido: {message}")

        if not conversation_history:
            return jsonify({"status": "error", "message": "No hay conversación activa"}), 500

        # Agregar mensaje del usuario al historial
        conversation_history.append({"role": "user", "content": message})
        
        # Construir el contexto completo
        context = MEDIATOR_PROMPT + "\n\nHistorial de conversación:\n"
        for msg in conversation_history:
            role = "Usuario" if msg["role"] == "user" else "Mediador"
            context += f"{role}: {msg['content']}\n"
        
        context += "\nMediador:"
        
        # Generar respuesta con Gemini
        response = model.generate_content(context)
        assistant_response = response.text
        
        # Agregar respuesta al historial
        conversation_history.append({"role": "assistant", "content": assistant_response})
        
        print(f"Respuesta del mediador: {assistant_response[:100]}...")
        
        return jsonify({
            "status": "success",
            "data": {
                "response": assistant_response
            }
        }), 200

    except Exception as e:
        error_msg = f"Error en send_message: {str(e)}"
        print(f"ERROR: {error_msg}")
        return jsonify({"status": "error", "message": error_msg}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "Backend funcionando correctamente con Gemini"}), 200

@app.route('/reset_conversation', methods=['POST'])
def reset_conversation():
    global conversation_history
    conversation_history = []
    return jsonify({"status": "success", "message": "Conversación reiniciada"}), 200

if __name__ == '__main__':
    print("Iniciando servidor Flask con Gemini...")
    app.run(debug=True, host='127.0.0.1', port=5000)
