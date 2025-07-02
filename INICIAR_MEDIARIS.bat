@echo off
echo.
echo =================================
echo   INICIANDO MEDIARIS 2.0
echo =================================
echo.

echo Verificando Python...
python --version

echo.
echo Cambiando al directorio backend...
cd backend

echo.
echo Verificando dependencias...
pip show flask > nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando dependencias...
    pip install -r requirements.txt
)

echo.
echo Iniciando servidor Flask...
echo.
echo ========================================
echo   SERVIDOR INICIADO EN:
echo   http://127.0.0.1:5000
echo.
echo   PARA USAR MEDIARIS:
echo   1. Abre index.html en tu navegador
echo   2. Haz clic en "Iniciar conversación"
echo   3. Presiona Ctrl+C para detener
echo ========================================
echo.

python app.py

pause
