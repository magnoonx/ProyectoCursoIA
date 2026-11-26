@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

set "PY_RUN=%~dp0python_portable\python.exe"
set "APP_DIR=%~dp0asistente_web"

REM 1. Detectar la IP local de este equipo en la red del aula
set "IP_LOCAL=127.0.0.1"
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /C:"IPv4"') do (
    for /f "tokens=1" %%b in ("%%a") do (
        set "IP_LOCAL=%%b"
    )
)

echo ==============================================================================
echo   Laboratorio IA - Interfaz Web (Puerto 5000)
echo   Modo: Red Local del Aula (PC + Celulares)
echo ==============================================================================
echo.
echo   Desde esta PC:      http://127.0.0.1:5000
echo   Desde celulares:    http://!IP_LOCAL!:5000
echo.
echo   Los alumnos deben conectar su celular a la misma WiFi del aula
echo   y abrir en Chrome o Safari:
echo.
echo      http://!IP_LOCAL!:5000
echo.
echo ==============================================================================

REM 2. Liberar puerto 5000 si quedo ocupado de una sesion anterior
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":5000" ^| findstr "LISTENING"') do (
    taskkill /F /PID %%a >nul 2>&1
)

REM 3. Abrir regla de firewall para que los celulares puedan conectarse
netsh advfirewall firewall show rule name="Laboratorio IA Puerto 5000" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Creando regla de Firewall para permitir acceso en el puerto 5000...
    netsh advfirewall firewall add rule name="Laboratorio IA Puerto 5000" dir=in action=allow protocol=TCP localport=5000 >nul 2>&1
    if errorlevel 1 (
        echo [AVISO] No se pudo crear la regla de firewall automaticamente.
        echo          Si los celulares no pueden conectarse, ejecute este BAT como Administrador
        echo          o agregue manualmente una regla de entrada TCP para el puerto 5000.
    ) else (
        echo [OK] Regla de firewall creada exitosamente.
    )
)

REM 4. Abrir el navegador de la PC del profesor tras 3 segundos
start "" cmd /c "timeout /t 3 >nul & start http://127.0.0.1:5000"

REM 5. Entrar a la carpeta asistente_web y ejecutar app.py
cd /d "%APP_DIR%"
if exist "%PY_RUN%" goto RUN_PORTABLE
python app.py
goto END

:RUN_PORTABLE
"%PY_RUN%" app.py

:END
echo.
echo [AVISO] El servidor web se detuvo.
pause
