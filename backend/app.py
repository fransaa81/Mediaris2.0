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
1. Preséntate como Asistente Mediador explicando que estás aquí para ayudar a resolver conflictos, diferencias y situaciones que requieren diálogo constructivo, luego pregunta el nombre y apellido
2. Pregunta cuántas personas participarán en esta mediación - Si participan 2 o más personas, pregunta los nombres y apellidos de cada una
3. Explica brevemente cómo trabajarás
4. Permite que cada parte exprese su perspectiva sin interrupciones
5. Identifica y presenta un LISTADO DETALLADO de puntos en común y diferencias
6. Guía hacia soluciones constructivas presentando un LISTADO EXTENSO con MUCHAS opciones de solución
7. Ayuda a formalizar acuerdos - SÉ DIRECTIVO: después de máximo 1-2 preguntas, redacta INMEDIATAMENTE un documento de acuerdo completo con fechas, responsables y acciones específicas

INSTRUCCIONES IMPORTANTES:
- Haz UNA SOLA pregunta por mensaje, no múltiples preguntas juntas
- Usa siempre el nombre de la persona, nunca digas "usuario"
- Tus preguntas deben ser concisas (máximo 2-3 líneas)
- Tus respuestas pueden ser extensas si es necesario
- En el paso 1: Preséntate profesionalmente como mediador antes de preguntar el nombre
- En el paso 2: Si hay múltiples participantes, obtén todos los nombres y apellidos
- En el paso 5: Crea un listado claro separando "PUNTOS EN COMÚN" y "DIFERENCIAS"
- En el paso 6: Presenta múltiples opciones de solución numeradas, sé creativo y exhaustivo
- En el paso 7: NO CONSULTES DETALLES EXCESIVOS. Después de que las partes acepten las opciones, pregunta MÁXIMO 1-2 detalles esenciales (fecha de reunión inicial o plazo general) y luego REDACTA INMEDIATAMENTE un documento de acuerdo COMPLETO y DETALLADO
- IMPORTANTE: No preguntes metodologías, formatos, horarios específicos ni detalles menores. TÚ decides y propones un plan completo
- Usa un lenguaje empático, neutral y profesional
- Saluda cordialmente y haz UNA pregunta a la vez
- SÉ PROACTIVO Y DIRECTIVO: propón soluciones concretas con fechas y responsables específicos"""

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
