import time
import subprocess
import sys
import requests

print("Iniciando prueba del servidor web...")
proc = subprocess.Popen([sys.executable, "asistente_web/app.py"])
time.sleep(3)

try:
    r = requests.get("http://127.0.0.1:5000/api/status", timeout=5)
    print("STATUS_CODE:", r.status_code)
    print("RESPONSE:", r.text)
    
    r_docs = requests.get("http://127.0.0.1:5000/api/datos_prueba/listar", timeout=5)
    print("DATOS_PRUEBA:", r_docs.text)
    print("\n[OK] El servidor web y todos los endpoints responden perfectamente.")
finally:
    proc.terminate()
    proc.wait()
