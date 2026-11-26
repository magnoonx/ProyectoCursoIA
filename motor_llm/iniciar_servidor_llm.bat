@echo off
setlocal enabledelayedexpansion

REM 1. Definir rutas base
set "BASE_DIR=%~dp0"
set "PY_RUN=%BASE_DIR%..\python_portable\python.exe"

pushd "%BASE_DIR%modelos"
set "MODELOS_DIR=%CD%"
popd

echo ==============================================================================
echo   Iniciando entorno del Motor LLM (llama.cpp Local)
echo ==============================================================================

REM 2. Escanear modelos .gguf disponibles en la carpeta 'modelos' (incluyendo subcarpetas de LM Studio)
set count=0
for /r "%MODELOS_DIR%" %%F in (*.gguf) do (
    set "fname=%%~nxF"
    if "!fname:~0,7!" neq "mmproj-" (
        set /a count+=1
        set "model_!count!=%%F"
        set "name_!count!=%%~nxF"
        
        set "full_dir=%%~dpF"
        set "sub_dir=!full_dir:%MODELOS_DIR%=!"
        if "!sub_dir!"=="\" (
            set "folder_!count!="
        ) else if "!sub_dir!"=="" (
            set "folder_!count!="
        ) else (
            set "sub_clean=!sub_dir:~1,-1!"
            set "folder_!count!=!sub_clean!"
        )
    )
)

REM 3. Si no hay modelos, ofrecer descarga de Qwen 2.5 3B
if %count% equ 0 goto NO_MODELS_FOUND
goto MODELS_FOUND

:NO_MODELS_FOUND
echo [ERROR] No se encontraron archivos de modelo .gguf en:
echo "%MODELOS_DIR%"
echo.
echo Intentando descargar el modelo base Qwen 2.5 3B...
if exist "%PY_RUN%" goto RUN_PORTABLE_DL
python "%BASE_DIR%descargar_qwen_3b.py"
goto END_DL

:RUN_PORTABLE_DL
"%PY_RUN%" "%BASE_DIR%descargar_qwen_3b.py"

:END_DL
for /r "%MODELOS_DIR%" %%F in (*.gguf) do (
    set "fname=%%~nxF"
    if "!fname:~0,7!" neq "mmproj-" (
        set /a count+=1
        set "model_!count!=%%F"
        set "name_!count!=%%~nxF"
    )
)
if %count% equ 0 (
    echo.
    echo [ERROR] No hay ningun modelo .gguf disponible en 'motor_llm\modelos\'.
    echo Puede descargar modelos desde LM Studio o copiarlos directamente a esta carpeta.
    pause
    exit /b 1
)

:MODELS_FOUND
REM 4. Seleccion interactiva de modelo si hay mas de uno
if %count% equ 1 (
    echo [INFO] 1 modelo detectado: !name_1!
    set "choice=1"
    goto MODEL_CHOSEN
)

echo.
echo Modelos LLM (.gguf) detectados en la carpeta 'modelos':
echo ------------------------------------------------------------------------------
for /l %%i in (1, 1, %count%) do (
    if "!folder_%%i!"=="" (
        echo   [%%i] !name_%%i!
    ) else (
        echo   [%%i] !name_%%i!  [!folder_%%i!]
    )
)
echo ------------------------------------------------------------------------------

set "choice="
if "%~1" neq "" (
    set "choice=%~1"
    echo [INFO] Seleccion automatica por parametro: %~1
) else (
    set /p "choice=Seleccione el modelo a cargar [1-%count%] (Enter para [1]): "
)

if "!choice!"=="" set "choice=1"

if not defined model_!choice! (
    echo [AVISO] Opcion '!choice!' no valida. Cargando modelo [1] por defecto.
    set "choice=1"
)

:MODEL_CHOSEN
set "MODEL_PATH=!model_%choice%!"
set "MODEL_NAME=!name_%choice%!"

echo.
echo [OK] Modelo seleccionado: !MODEL_NAME!
echo Ruta: "!MODEL_PATH!"
echo.

:DETECT_ENGINE
REM 5. Deteccion automatica de compatibilidad de CPU (Universal con auto-dispatch de arquitectura)
set "LLAMA_BIN="
set "LLAMA_MODE="

REM Probar 1: bin principal (Nueva version universal con dynamic CPU dispatch)
if exist "%BASE_DIR%bin\llama-server.exe" (
    "%BASE_DIR%bin\llama-server.exe" --version >nul 2>&1
    if not errorlevel 1 (
        set "LLAMA_BIN=%BASE_DIR%bin\llama-server.exe"
        set "LLAMA_MODE=Universal (Auto-deteccion de microarquitectura CPU)"
        goto ENGINE_READY
    )
)

REM Probar 2: bin_avx (Compatibilidad Sandy/Ivy Bridge, AMD FX)
if exist "%BASE_DIR%bin_avx\llama-server.exe" (
    "%BASE_DIR%bin_avx\llama-server.exe" --version >nul 2>&1
    if not errorlevel 1 (
        echo [INFO] Probando motor de compatibilidad AVX1...
        set "LLAMA_BIN=%BASE_DIR%bin_avx\llama-server.exe"
        set "LLAMA_MODE=AVX (Compatibilidad Media)"
        goto ENGINE_READY
    )
)

REM Probar 3: bin_noavx (Universal Celeron, Pentium, procesadores antiguos)
if exist "%BASE_DIR%bin_noavx\llama-server.exe" (
    "%BASE_DIR%bin_noavx\llama-server.exe" --version >nul 2>&1
    if not errorlevel 1 (
        echo [INFO] Probando motor universal NO-AVX...
        set "LLAMA_BIN=%BASE_DIR%bin_noavx\llama-server.exe"
        set "LLAMA_MODE=NO-AVX (Universal / Celeron / Pentium)"
        goto ENGINE_READY
    )
)

goto NO_COMPATIBLE_ENGINE

:ENGINE_READY
echo [INFO] Motor seleccionado: !LLAMA_MODE!
echo [INFO] Liberando instancias previas en el puerto 8081...
taskkill /F /IM llama-server.exe /T >nul 2>&1

echo [INFO] Iniciando servidor LLM en 127.0.0.1:8081 (solo acceso interno)...
echo Parametros: -m "!MODEL_PATH!" -c 4096 -t 2 --port 8081
echo.
echo ==============================================================================
echo   Motor LLM activo con: !MODEL_NAME!
echo   Modulos disponibles del Laboratorio:
echo   - [AUDIO] Transcriptor y Asistente de Voz
echo   - [PDF]   Lector y Auditor de PDFs
echo   - [DATOS] Analista de Hojas de Calculo (Excel/CSV)
echo.
echo   PASO SIGUIENTE: Abra 00_INICIAR_LABORATORIO.bat en otra ventana.
echo   Los alumnos podran acceder desde sus celulares a traves de la WiFi.
echo ==============================================================================
echo.

"!LLAMA_BIN!" -m "!MODEL_PATH!" -c 4096 -t 2 -tb 2 --host 127.0.0.1 --port 8081
set "SERVER_EXIT=!ERRORLEVEL!"

if !SERVER_EXIT! equ 0 goto SERVER_OK
goto SERVER_ERROR

:SERVER_OK
echo.
echo [INFO] Servidor detenido normalmente por el usuario.
pause
exit /b 0

:SERVER_ERROR
echo.
echo ==============================================================================
echo [ERROR] El servidor LLM no pudo iniciar o se cerro (Codigo de salida: !SERVER_EXIT!).
echo ==============================================================================
if "!SERVER_EXIT!"=="-1073741795" echo Causa: Instruccion de CPU incompatible.
if "!SERVER_EXIT!"=="3221225501"  echo Causa: Instruccion de CPU incompatible.
if "!SERVER_EXIT!"=="-1073741515" echo Causa: Faltan librerias del sistema (Visual C++ 2015-2022).
if "!SERVER_EXIT!"=="3221225781"  echo Causa: Faltan librerias del sistema (Visual C++ 2015-2022).
if "!SERVER_EXIT!"=="1"           echo Causa: Incompatibilidad de arquitectura o memoria insuficiente para este modelo.
echo.
echo Opciones recomendadas:
echo [A] Para modelos con arquitectura propietaria o muy nuevos, use LM Studio en puerto 1234.
echo [B] Si la PC tiene poca memoria RAM, elija un modelo mas liviano (ej: Qwen 2.5 3B o Llama 3.2 3B).
echo ==============================================================================
pause
exit /b !SERVER_EXIT!

:NO_COMPATIBLE_ENGINE
echo.
echo ==============================================================================
echo [ERROR CRITICO] No se pudo ejecutar ninguna version de 'llama-server.exe'.
echo ==============================================================================
echo Causas frecuentes en equipos con Windows 10:
echo.
echo [1] Falta el paquete Microsoft Visual C++ 2015-2022 Redistributable (x64).
echo [2] SmartScreen / Windows Defender bloqueo la ejecucion del archivo.
echo [3] Alternativa: Abra LM Studio, cargue el modelo y active el servidor en puerto 1234.
echo ==============================================================================
pause
exit /b 1
