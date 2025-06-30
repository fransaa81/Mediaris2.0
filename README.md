# MEDIARIS - Sistema de Mediación Digital

MEDIARIS es una plataforma web que utiliza inteligencia artificial para facilitar procesos de mediación social en conflictos familiares, de pareja, entre amistades y grupales.

## 🚀 Características

- **Interfaz web moderna** con diseño responsive
- **Chatbot inteligente** powered by OpenAI GPT
- **Diferentes tipos de mediación** para distintas situaciones
- **Sistema backend robusto** con Flask y Python
- **Conectores directos** a la API de OpenAI

## 📋 Requisitos Previos

- Python 3.8 o superior
- Una API key de OpenAI
- Navegador web moderno

## ⚙️ Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone [URL_DEL_REPOSITORIO]
cd Mediaris
```

### 2. Configurar el Backend

#### Instalar dependencias de Python:
```bash
cd backend
pip install -r requirements.txt
```

#### Configurar la API Key de OpenAI:
1. Copia el archivo de ejemplo:
   ```bash
   cp api_key.env.example api_key.env
   ```
2. Edita `backend/api_key.env` y reemplaza `TU_API_KEY_AQUI` con tu API key real:
   ```
   API_KEY=sk-tu-api-key-real-aqui
   ```
3. Obtén tu API key en: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)

#### Ejecutar el servidor backend:
```bash
python app.py
```

Deberías ver:
```
✅ Conexión con OpenAI verificada correctamente
* Running on http://127.0.0.1:5000
```

### 3. Ejecutar el Frontend

1. Abre `index.html` en tu navegador web
2. O usa un servidor web local como Live Server (extensión de VS Code)

## 🎯 Uso del Sistema

1. **Navegar por la web:** Explora las secciones de Servicios, Nosotros y Contacto
2. **Usar el Chatbot:** Haz clic en "Iniciar conversación"
3. **Interactuar:** El asistente te guiará a través del proceso de mediación

## 🔧 Solución de Problemas

### Error: "Failed to fetch"
- **Causa:** El servidor backend no está ejecutándose
- **Solución:** Ejecuta `python app.py` en la carpeta backend

### Error: "El cliente de OpenAI no está disponible"
- **Causa:** La API key no está configurada correctamente
- **Solución:** Verifica el archivo `api_key.env` con tu API key real

### Error: "No hay conversación activa"
- **Causa:** El thread de conversación se perdió
- **Solución:** Cierra y vuelve a abrir el chatbot

## 📁 Estructura del Proyecto

```
Mediaris/
├── index.html              # Página principal
├── css/
│   └── styles.css          # Estilos del sitio
├── js/
│   └── bot.js             # Lógica del chatbot
├── img/
│   └── imagen-mediaris.png # Recursos gráficos
├── backend/
│   ├── app.py             # Servidor Flask
│   ├── requirements.txt   # Dependencias Python
│   ├── api_key.env        # Configuración API key (NO SUBIR A GIT)
│   └── api_key.env.example # Ejemplo de configuración
├── setup.bat              # Script de configuración automática
└── README.md              # Este archivo
```

## 🔒 Seguridad

- ⚠️ **IMPORTANTE:** Nunca subas tu archivo `api_key.env` al repositorio
- 🔐 Tu API key es confidencial y tiene costos asociados
- 📝 El archivo `api_key.env` está incluido en `.gitignore`

## 💡 Notas Importantes

- **Costos:** Usar la API de OpenAI tiene costos asociados
- **Desarrollo:** Para desarrollo, puedes usar `debug=True` en Flask
- **Producción:** Para producción, cambia las configuraciones de seguridad
- **Limitaciones:** Esta plataforma es para mediación social, no reemplaza servicios profesionales

## 🚀 Despliegue

Para desplegar en producción:

1. Configura variables de entorno en tu servidor
2. Usa un servidor WSGI como Gunicorn
3. Configura HTTPS
4. Ajusta la configuración de CORS según sea necesario

## 📞 Contacto y Soporte

Si tienes problemas con la configuración:
1. Verifica que todas las dependencias estén instaladas
2. Confirma que la API key sea válida
3. Revisa que no haya otros servicios usando el puerto 5000
4. Consulta los mensajes de error en la consola del navegador (F12)

---

© 2025 Mediaris. Todos los derechos reservados.
