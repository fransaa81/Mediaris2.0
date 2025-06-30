@echo off
echo ========================================
echo    MEDIARIS - Configuracion Inicial
echo ========================================
echo.

echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH.
    echo Por favor instala Python 3.8 o superior desde python.org
    pause
    exit /b 1
)

echo Python encontrado!
echo.

echo Instalando dependencias...
cd backend
pip install -r requirements.txt

echo.
echo ========================================
echo   CONFIGURACION DE API KEY
echo ========================================
echo.

if not exist api_key.env (
    echo Creando archivo de configuracion...
    copy api_key.env.example api_key.env
    echo.
    echo ARCHIVO CREADO: backend\api_key.env
    echo.
) else (
    echo El archivo api_key.env ya existe.
    echo.
)

echo IMPORTANTE: Debes configurar tu API key de OpenAI:
echo.
echo 1. Obtener una API key desde: https://platform.openai.com/api-keys
echo 2. Abrir el archivo: backend\api_key.env
echo 3. Reemplazar "TU_API_KEY_AQUI" con tu API key real
echo.
echo Ejemplo:
echo   API_KEY=sk-1234567890abcdef...
echo.
echo ========================================

set /p respuesta="¿Has configurado tu API key? (s/n): "
if /i "%respuesta%"=="s" (
    echo.
    echo Iniciando servidor backend...
    python app.py
) else (
    echo.
    echo Por favor configura tu API key primero, luego ejecuta:
    echo   cd backend
    echo   python app.py
    echo.
    echo O ejecuta este script nuevamente.
)

pause
