# 🏛️ MEDIARIS 2.0 - Guía de Uso

## 📋 **Estado del Proyecto**
✅ **COMPLETAMENTE CONFIGURADO Y FUNCIONANDO**

- ✅ Backend Flask con Google Gemini
- ✅ Frontend HTML/CSS/JavaScript
- ✅ Integración completa bot ↔ backend
- ✅ Sin dependencias de OpenAI
- ✅ Archivos duplicados eliminados

---

## 🚀 **Cómo iniciar el sistema**

### 1️⃣ **Iniciar el Backend**
```bash
# Navegar al directorio backend
cd "c:\Users\Casa de San Luis\OneDrive\Escritorio\Mediaris 2.0\backend"

# Iniciar el servidor Flask
python app.py
```

### 2️⃣ **Abrir el Frontend**
- Abrir el archivo `index.html` en tu navegador
- O usar la URL: `file:///c:/Users/Casa%20de%20San%20Luis/OneDrive/Escritorio/Mediaris%202.0/index.html`

### 3️⃣ **Probar la funcionalidad**
1. En el navegador, hacer clic en "Iniciar conversación"
2. El bot debería conectarse automáticamente con Gemini
3. Comenzar a chatear con el mediador virtual

---

## 🔧 **Estructura Final del Proyecto**

```
Mediaris 2.0/
├── backend/
│   ├── acuerdos/          # Almacena acuerdos generados
│   ├── app.py             # ✅ Servidor Flask principal (SOLO GEMINI)
│   ├── api_key.env        # ✅ API Key de Gemini
│   └── requirements.txt   # ✅ Dependencias Python
├── css/
│   └── styles.css         # Estilos del frontend
├── js/
│   └── bot.js             # ✅ Cliente JavaScript (GEMINI)
├── img/
│   └── imagen-mediaris.png
├── index.html             # ✅ Página principal
├── README.md
└── .gitignore            # ✅ Actualizado para Gemini
```

---

## 🧪 **Pruebas de funcionamiento**

### ✅ **Backend Health Check**
```bash
curl http://127.0.0.1:5000/health
```
**Respuesta esperada:**
```json
{
  "message": "Backend funcionando correctamente con Gemini",
  "status": "ok"
}
```

### ✅ **Test de conversación**
1. Abrir el navegador con `index.html`
2. Hacer clic en "Iniciar conversación"
3. Debería aparecer un saludo del mediador
4. Escribir un mensaje y verificar respuesta

---

## 🔐 **Configuración de API Key**

El archivo `backend/api_key.env` contiene:
```
GEMINI_API_KEY=tu_api_key_aqui
```

---

## 📝 **Archivos eliminados/limpiados**

- ❌ `app_clean.py` (duplicado)
- ❌ `app_gemini.py` (duplicado)
- ❌ `__pycache__/` (cache innecesario)
- ✅ Comentarios de OpenAI corregidos en `bot.js`

---

## 🎯 **Sistema listo para:**

1. **Desarrollo**: Hacer cambios y mejoras
2. **Pruebas**: Funcionalidad completa disponible
3. **Producción**: Con configuraciones adicionales de seguridad

---

## 🚨 **Solución de problemas**

### Backend no inicia:
```bash
# Verificar dependencias
pip install -r requirements.txt

# Verificar API key
echo $GEMINI_API_KEY
```

### Frontend no conecta:
- Verificar que el backend esté en `http://127.0.0.1:5000`
- Revisar consola del navegador para errores

### Chat no responde:
- Verificar API key de Gemini
- Revisar logs del servidor Flask

---

**✅ ESTADO: SISTEMA COMPLETAMENTE FUNCIONAL CON GEMINI**
