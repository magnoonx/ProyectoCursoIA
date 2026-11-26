@echo off
title Transcriptor Whisper Offline (Arrastrar y Soltar)
chcp 65001 >nul
cls

set PORTABLE_PY=%~dp0..\python_portable\python.exe
if exist "%PORTABLE_PY%" (
    set PY_CMD="%PORTABLE_PY%"
) else (
    set PY_CMD=python
)

if "%~1"=="" (
    echo ======================================================================
    echo           TRANSCRIPTOR WHISPER LOCAL (MODO DEMOSTRACIÓN)
    echo ======================================================================
    echo.
    echo Consejo: Puede arrastrar y soltar cualquier archivo de audio (.wav/.mp3)
    echo directamente sobre este archivo '.bat' para transcribirlo al instante.
    echo.
    echo Procesando audio de prueba por defecto...
    echo.
    %PY_CMD% "%~dp0transcribir.py"
) else (
    echo ======================================================================
    echo                  PROCESANDO AUDIO SELECCIONADO
    echo ======================================================================
    echo Archivo: %~1
    echo.
    %PY_CMD% "%~dp0transcribir.py" "%~1"
)

echo.
echo Presione cualquier tecla para salir...
pause >nul
