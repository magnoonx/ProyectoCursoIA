import os
import urllib.request
import json
import zipfile

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIN_DIR = os.path.join(BASE_DIR, "transcriptor_whisper", "bin")
os.makedirs(BIN_DIR, exist_ok=True)

def descargar_whisper_bin():
    print("Buscando binarios de whisper.cpp para Windows...")
    api_url = "https://api.github.com/repos/ggerganov/whisper.cpp/releases/latest"
    req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        zip_url = None
        for a in data.get("assets", []):
            name = a["name"].lower()
            if "bin-x64.zip" in name or "bin-win-x64.zip" in name or "whisper-bin-x64" in name:
                zip_url = a["browser_download_url"]
                break
        if not zip_url:
            zip_url = "https://github.com/ggerganov/whisper.cpp/releases/download/v1.7.4/whisper-bin-x64.zip"
        
        print(f"Descargando: {zip_url}...")
        zip_dest = os.path.join(BIN_DIR, "whisper_bin.zip")
        urllib.request.urlretrieve(zip_url, zip_dest)
        with zipfile.ZipFile(zip_dest, 'r') as zf:
            zf.extractall(BIN_DIR)
        if os.path.exists(zip_dest):
            os.remove(zip_dest)
        print("[OK] Binarios de whisper.cpp listos en transcriptor_whisper/bin/")
    except Exception as e:
        print("Error descargando whisper.cpp:", e)

if __name__ == "__main__":
    descargar_whisper_bin()
