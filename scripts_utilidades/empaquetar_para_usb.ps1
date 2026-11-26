# ==============================================================================
# Script de Empaquetado para Memoria USB del Laboratorio
# Crea una copia limpia o archivo comprimido listo para transferir a los equipos
# ==============================================================================

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "     EMPAQUETADOR DEL LABORATORIO DE OFIMÁTICA PARA MEMORIA USB       " -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

$BasePath = Split-Path -Parent $MyInvocation.MyCommand.Path
$BaseProject = Split-Path -Parent $BasePath

$DestinoUSB = Read-Host "Ingrese la letra o ruta de la memoria USB (ej: E:\ o C:\LabOffline)"

if ([string]::IsNullOrWhiteSpace($DestinoUSB)) {
    Write-Host "Operación cancelada. No se especificó ruta de destino." -ForegroundColor Yellow
    exit 0
}

if (-not (Test-Path $DestinoUSB)) {
    New-Item -ItemType Directory -Force -Path $DestinoUSB | Out-Null
}

$DestinoFinal = Join-Path $DestinoUSB "ProyectoCursoIA"
Write-Host "`nCopiando archivos del proyecto hacia: $DestinoFinal ..." -ForegroundColor Yellow

# Excluir temporales de Python como __pycache__
$exclude = @("__pycache__", "*.pyc", ".git", "uploads")

robocopy $BaseProject $DestinoFinal /E /XD __pycache__ .git uploads /XF *.pyc *.log /NP

Write-Host "`n[OK] Copia completada exitosamente en la memoria USB." -ForegroundColor Green
Write-Host "Para desplegar en las computadoras del aula:" -ForegroundColor Cyan
Write-Host "1. Copie la carpeta 'ProyectoCursoIA' al disco local del equipo del alumno."
Write-Host "2. Ejecute '00_INICIAR_LABORATORIO.bat'." -ForegroundColor White
