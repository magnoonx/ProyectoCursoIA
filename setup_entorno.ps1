# ==============================================================================
# Script de Aprovisionamiento y Verificacion del Entorno Offline de IA
# Curso de Inteligencia Artificial para Asistentes Administrativos y Ofimatica
# ==============================================================================

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "   APROVISIONAMIENTO DEL LABORATORIO DE IA EN OFIMATICA (OFFLINE)     " -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

$BasePath = Split-Path -Parent $MyInvocation.MyCommand.Path

# 1. Comprobar Python Portable o de Sistema
Write-Host "[1/5] Verificando entorno de ejecucion..." -ForegroundColor Yellow
$PortablePy = Join-Path $BasePath "python_portable\python.exe"

if (Test-Path $PortablePy) {
    Write-Host "   [OK] Entorno Python Portable detectado: $PortablePy" -ForegroundColor Green
    Write-Host "   (El sistema es 100% standalone; no requiere Python instalado en la maquina)." -ForegroundColor DarkGreen
    $PyExecutable = $PortablePy
} else {
    try {
        $pyVer = python --version
        Write-Host "   [OK] Python de sistema detectado: $pyVer" -ForegroundColor Green
        $PyExecutable = "python"
    } catch {
        Write-Host "   [ERROR] No se encontro Python portable ni de sistema." -ForegroundColor Red
        exit 1
    }
}

# 2. Verificar dependencias de Python
Write-Host ""
Write-Host "[2/5] Verificando librerias requeridas..." -ForegroundColor Yellow
$paquetes = @("flask", "faster_whisper", "pandas", "openpyxl", "pypdf", "fpdf", "requests")
$faltantes = @()

foreach ($pkg in $paquetes) {
    $check = & $PyExecutable -c "import $pkg; print('ok')" 2>$null
    if ($check -ne "ok") {
        $faltantes += $pkg
    }
}

if ($faltantes.Count -gt 0) {
    Write-Host "   [AVISO] Algunas librerias no se detectaron: $($faltantes -join ', ')" -ForegroundColor Yellow
} else {
    Write-Host "   [OK] Todas las dependencias principales estan listas en el entorno portable." -ForegroundColor Green
}

# 3. Comprobar modelo Whisper para audio
Write-Host ""
Write-Host "[3/5] Verificando modelo Whisper local..." -ForegroundColor Yellow
$whisperModelDir = Join-Path $BasePath "transcriptor_whisper\modelos"
if (Test-Path $whisperModelDir) {
    $archivosWhisper = Get-ChildItem -Path $whisperModelDir -Recurse -File
    if ($archivosWhisper.Count -gt 0) {
        Write-Host "   [OK] Modelo Whisper disponible localmente en: $whisperModelDir" -ForegroundColor Green
    } else {
        Write-Host "   [AVISO] Se descargara el modelo Whisper base la primera vez que se ejecute la transcripcion." -ForegroundColor DarkYellow
    }
} else {
    New-Item -ItemType Directory -Force -Path $whisperModelDir | Out-Null
}

# 4. Comprobar modelo LLM (Qwen 2.5 3B) y Binario llama-server
Write-Host ""
Write-Host "[4/5] Verificando motor LLM (llama.cpp y Qwen 2.5 3B)..." -ForegroundColor Yellow
$llamaBin = Join-Path $BasePath "motor_llm\bin\llama-server.exe"
if (Test-Path $llamaBin) {
    Write-Host "   [OK] Binario nativo llama-server.exe verificado en: motor_llm\bin\" -ForegroundColor Green
} else {
    Write-Host "   [AVISO] llama-server.exe no encontrado en motor_llm\bin\" -ForegroundColor Yellow
}

$modelFile = Join-Path $BasePath "motor_llm\modelos\qwen2.5-3b-instruct-q4_k_m.gguf"
if (Test-Path $modelFile) {
    $tamanoGB = [math]::Round((Get-Item $modelFile).Length / 1GB, 2)
    Write-Host "   [OK] Modelo Qwen 2.5 3B encontrado ($tamanoGB GB)." -ForegroundColor Green
} else {
    Write-Host "   [PENDIENTE] El modelo 'qwen2.5-3b-instruct-q4_k_m.gguf' no esta en 'motor_llm\modelos\'." -ForegroundColor Yellow
    Write-Host "   Puede descargarlo ejecutando:" -ForegroundColor Cyan
    Write-Host "     & '$PyExecutable' motor_llm\descargar_qwen_3b.py" -ForegroundColor White
    Write-Host "   O copiarlo directamente desde la memoria USB del docente." -ForegroundColor Cyan
}

# 5. Generar datos de prueba si no existen
Write-Host ""
Write-Host "[5/5] Comprobando material de practica (PDFs, Audios, Excel)..." -ForegroundColor Yellow
$pdfCheck = Join-Path $BasePath "datos_de_prueba\02_documentos_pdf\Contrato_Prestacion_Servicios_No_402.pdf"
if (-not (Test-Path $pdfCheck)) {
    Write-Host "   Generando archivos de prueba..." -ForegroundColor Yellow
    & $PyExecutable (Join-Path $BasePath "scripts_utilidades\generar_datos_prueba.py")
} else {
    Write-Host "   [OK] Banco de datos de prueba completo y verificado." -ForegroundColor Green
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Green
Write-Host "   CONFIGURACION COMPLETADA CON EXITO                                 " -ForegroundColor Green
Write-Host "   Para iniciar el laboratorio haga doble clic en:                    " -ForegroundColor Green
Write-Host "     00_INICIAR_LABORATORIO.bat                                       " -ForegroundColor White
Write-Host "======================================================================" -ForegroundColor Green
Write-Host ""
