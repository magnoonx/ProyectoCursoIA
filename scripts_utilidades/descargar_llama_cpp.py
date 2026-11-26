"""
Descargador de binarios portables y universales de llama.cpp para Windows:
- bin (AVX2 x64): Máximo rendimiento para procesadores modernos (Intel Core 4ta+ gen, AMD Ryzen)
- bin_avx (AVX x64): Alta compatibilidad (Intel Core 2da y 3ra gen Sandy/Ivy Bridge, AMD FX)
- bin_noavx (NO-AVX x64): Compatibilidad universal (Intel Celeron, Pentium, procesadores legacy)

Copia automáticamente las librerías de tiempo de ejecución de Visual C++ (MSVCP140, VCRUNTIME140)
para garantizar funcionamiento 100% portable y offline en equipos sin software previo.
"""
import os
import sys
import shutil
import zipfile
import urllib.request
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOTOR_DIR = os.path.join(BASE_DIR, "motor_llm")

VC_DLLS = [
    r"C:\Windows\System32\msvcp140.dll",
    r"C:\Windows\System32\msvcp140_codecvt_ids.dll",
    r"C:\Windows\System32\vcruntime140.dll",
    r"C:\Windows\System32\vcruntime140_1.dll",
    r"C:\Windows\System32\vcomp140.dll"
]

VARIANTS = [
    {
        "id": "bin",
        "pattern": "bin-win-avx2-x64",
        "fallback": "https://github.com/ggerganov/llama.cpp/releases/download/b4600/llama-b4600-bin-win-avx2-x64.zip",
        "desc": "AVX2 (Modo Optimizado)"
    },
    {
        "id": "bin_avx",
        "pattern": "bin-win-avx-x64",
        "fallback": "https://github.com/ggerganov/llama.cpp/releases/download/b4600/llama-b4600-bin-win-avx-x64.zip",
        "desc": "AVX (Intel Core 2da/3ra gen, AMD FX)"
    },
    {
        "id": "bin_noavx",
        "pattern": "bin-win-noavx-x64",
        "fallback": "https://github.com/ggerganov/llama.cpp/releases/download/b4600/llama-b4600-bin-win-noavx-x64.zip",
        "desc": "NO-AVX (Universal / Celeron / Pentium)"
    }
]

def copiar_vc_dlls(target_dir):
    for dll in VC_DLLS:
        if os.path.exists(dll):
            try:
                shutil.copy2(dll, target_dir)
            except Exception:
                pass

def descargar_llama_server():
    print("=" * 65)
    print(" CONFIGURACIÓN DEL MOTOR UNIVERSAL LLAMA.CPP (PORTABLE OFFLINE)")
    print("=" * 65)

    headers = {"User-Agent": "Mozilla/5.0"}
    latest_assets = []
    try:
        api_url = "https://api.github.com/repos/ggerganov/llama.cpp/releases/latest"
        req = urllib.request.Request(api_url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode())
            latest_assets = data.get("assets", [])
    except Exception:
        pass

    for variant in VARIANANTS if 'VARIANANTS' in locals() else VARIANTS:
        dest_dir = os.path.join(MOTOR_DIR, variant["id"])
        server_exe = os.path.join(dest_dir, "llama-server.exe")
        os.makedirs(dest_dir, exist_ok=True)

        if os.path.exists(server_exe):
            print(f"[OK] {variant['desc']} ya instalado en: {variant['id']}/")
            copiar_vc_dlls(dest_dir)
            continue

        zip_url = None
        for asset in latest_assets:
            name = asset.get("name", "").lower()
            if variant["pattern"] in name and name.endswith(".zip"):
                zip_url = asset.get("browser_download_url")
                break

        if not zip_url:
            zip_url = variant["fallback"]

        print(f"Descargando {variant['desc']}...")
        zip_path = os.path.join(dest_dir, "pkg.zip")
        try:
            req = urllib.request.Request(zip_url, headers=headers)
            with urllib.request.urlopen(req, timeout=60) as resp, open(zip_path, "wb") as f:
                while True:
                    chunk = resp.read(64 * 1024)
                    if not chunk:
                        break
                    f.write(chunk)

            print(f"Descomprimiendo en motor_llm/{variant['id']}/...")
            with zipfile.ZipFile(zip_path, 'r') as zf:
                zf.extractall(dest_dir)

            if os.path.exists(zip_path):
                os.remove(zip_path)

            copiar_vc_dlls(dest_dir)
            print(f"[OK] {variant['desc']} instalado exitosamente.")
        except Exception as e:
            print(f"[AVISO] No se pudo descargar {variant['desc']}: {e}")

    print("=" * 65)
    print("Todos los binarios y dependencias runtime quedaron configurados.")
    return True

if __name__ == "__main__":
    descargar_llama_server()
