# 🏛️ MEDIARIS 2.0

**Sistema de Mediación Social con Inteligencia Artificial**

MEDIARIS es una plataforma web que integra un asistente de IA especializado en mediación de conflictos, diseñado para ayudar a resolver disputas familiares, entre amistades y en espacios comunitarios.

## 🚀 **Características**

- ✅ **Asistente IA con Google Gemini** - Mediador virtual profesional
- ✅ **Interfaz web moderna** - Diseño responsivo y accesible
- ✅ **Especialización en conflictos** - Familiares, amistad, comunitarios
- ✅ **Proceso estructurado** - Metodología profesional de mediación
- ✅ **100% Gratuito** - Sin costos de API (Gemini free tier)

## 🛠️ **Tecnologías**

- **Backend**: Python + Flask + Google Gemini AI
- **Frontend**: HTML5 + CSS3 + JavaScript
- **IA**: Google Gemini 1.5 Flash (Gratuito)

## ⚡ **Instalación Rápida**

### 1️⃣ **Clonar repositorio**
```bash
git clone [url-repositorio]
cd "Mediaris 2.0"
```

### 2️⃣ **Configurar Python**
```bash
cd backend
pip install -r requirements.txt
```

### 3️⃣ **Configurar API Key**
1. Obtén tu API key gratuita en: https://makersuite.google.com/app/apikey
2. Edita `backend/api_key.env`:
```env
GEMINI_API_KEY=tu_api_key_aqui
```

### 4️⃣ **Iniciar sistema**
```bash
# Terminal 1: Backend
cd backend
python app.py

# Terminal 2: Frontend
# Abrir index.html en navegador
```

## 🎯 **Uso**

1. **Abrir** `index.html` en tu navegador
2. **Hacer clic** en "Iniciar conversación"
3. **Chatear** con el mediador virtual
4. **Seguir** las recomendaciones del asistente

## 📁 **Estructura del Proyecto**

```
Mediaris 2.0/
├── backend/
│   ├── app.py              # Servidor Flask principal
│   ├── api_key.env         # Configuración API Gemini
│   ├── requirements.txt    # Dependencias Python
│   └── acuerdos/          # Almacén de acuerdos
├── css/
│   └── styles.css         # Estilos principales
├── js/
│   └── bot.js             # Cliente JavaScript
├── img/
│   └── imagen-mediaris.png
├── index.html             # Página principal
└── README.md              # Esta documentación
```

## 🔧 **API Endpoints**

- `POST /start_assistant` - Iniciar conversación
- `POST /send_message` - Enviar mensaje
- `POST /reset_conversation` - Reiniciar conversación
- `GET /health` - Estado del servidor

## 🧪 **Pruebas**

### Verificar backend:
```bash
curl http://127.0.0.1:5000/health
```

### Verificar frontend:
1. Abrir navegador en `index.html`
2. Probar chat del mediador

## 🔐 **Seguridad**

- ✅ API key protegida en `.env`
- ✅ CORS configurado correctamente
- ✅ Validación de entrada en endpoints
- ✅ `.gitignore` protege información sensible

## 🚨 **Solución de Problemas**

### Backend no inicia:
```bash
pip install -r requirements.txt
```

### Chat no responde:
1. Verificar API key en `api_key.env`
2. Comprobar que el backend esté en puerto 5000
3. Revisar consola del navegador (F12)

### Error 500:
- Verificar conexión a internet
- Comprobar validez de la API key de Gemini

## 📞 **Soporte**

Para problemas técnicos:
1. Revisar logs del servidor Flask
2. Comprobar consola del navegador
3. Verificar configuración de API key

## 📝 **Licencia**

Proyecto de código abierto para mediación social.

---

**✅ SISTEMA COMPLETAMENTE FUNCIONAL CON GOOGLE GEMINI**

*Última actualización: Julio 2025*
