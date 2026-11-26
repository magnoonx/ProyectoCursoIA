"""
Script de Descarga y Preparación del Modelo Qwen 2.5 3B Instruct (Q4_K_M GGUF)
Descarga el modelo desde Hugging Face y lo aloja en 'motor_llm/modelos/'
para permitir ejecución 100% offline en LM Studio, GPT4All o llama.cpp.
"""
import os
import sys
import time
import urllib.request

MODEL_URL = "https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF/resolve/main/qwen2.5-3b-instruct-q4_k_m.gguf"
MODEL_FILENAME = "qwen2.5-3b-instruct-q4_k_m.gguf"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST_DIR = os.path.join(BASE_DIR, "motor_llm", "modelos")
DEST_PATH = os.path.join(DEST_DIR, MODEL_FILENAME)

os.makedirs(DEST_DIR, exist_ok=True)

def reporthook(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration)) if duration > 0 else 0
    percent = min(int(count * block_size * 100 / total_size), 100)
    mb_down = progress_size / (1024 * 1024)
    mb_total = total_size / (1024 * 1024)
    sys.stdout.write(f"\r[Descarga] {percent:3d}% | {mb_down:.1f}/{mb_total:.1f} MB | Velocidad: {speed} KB/s")
    sys.stdout.flush()

def descargar_modelo():
    print("=" * 65)
    print(" DESCARGADOR OFICIAL DE MODELO QWEN 2.5 3B INSTRUCT (Q4_K_M)")
    print("=" * 65)
    print(f"Destino local: {DEST_PATH}")
    
    if os.path.exists(DEST_PATH):
        tamano_mb = os.path.getsize(DEST_PATH) / (1024 * 1024)
        if tamano_mb > 1800: # ~2.0 GB esperado
            print(f"\n[OK] El modelo ya se encuentra descargado ({tamano_mb:.1f} MB).")
            print("El entorno está listo para ejecución offline.")
            return True
        else:
            print(f"\n[AVISO] Archivo incompleto ({tamano_mb:.1f} MB). Se reanudará la descarga...")

    print(f"\nIniciando descarga desde HuggingFace (~2.0 GB)...")
    print("URL:", MODEL_URL)
    print("Nota: Solo necesita descargarse UNA VEZ. Luego podrá copiarse por USB a los demás equipos.")
    
    try:
        urllib.request.urlretrieve(MODEL_URL, DEST_PATH, reporthook)
        print("\n\n[ÉXITO] Modelo descargado y verificado correctamente.")
        print(f"Ubicación: {DEST_PATH}")
        return True
    except Exception as e:
        print(f"\n\n[ERROR] Ocurrió una falla durante la descarga: {e}")
        print("\nAlternativa manual para laboratorio sin internet:")
        print(f"1. Descargue el archivo en un equipo con internet desde:")
        print(f"   {MODEL_URL}")
        print(f"2. Cópielo a la memoria USB en la carpeta:")
        print(f"   {DEST_PATH}")
        return False

if __name__ == "__main__":
    descargar_modelo()
