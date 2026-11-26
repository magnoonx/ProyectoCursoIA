"""
Constructor del Entorno Python Portable para el Laboratorio Offline de IA.
Copia un intérprete Python 100% autocontenido y portable dentro de 'python_portable/'
para garantizar que el proyecto funcione en cualquier PC con Windows sin instalar nada.
"""
import os
import shutil
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORTABLE_DIR = os.path.join(BASE_DIR, "python_portable")
PY_SOURCE = r"C:\Python314"
USER_SITE = os.path.expanduser(r"~\AppData\Roaming\Python\Python314\site-packages")

def construir():
    print("=" * 65)
    print(" CONSTRUYENDO ENTORNO PYTHON PORTABLE (STANDALONE 100%)")
    print("=" * 65)
    print(f"Destino: {PORTABLE_DIR}")

    os.makedirs(PORTABLE_DIR, exist_ok=True)

    # 1. Copiar ejecutables y DLLs raíz
    archivos_raiz = [
        "python.exe", "pythonw.exe", "python3.dll", "python314.dll",
        "vcruntime140.dll", "vcruntime140_1.dll", "LICENSE.txt"
    ]
    for ar in archivos_raiz:
        src = os.path.join(PY_SOURCE, ar)
        dst = os.path.join(PORTABLE_DIR, ar)
        if os.path.exists(src):
            shutil.copy2(src, dst)
    print("[1/4] Ejecutables base y DLLs copiados.")

    # 2. Copiar carpeta DLLs
    src_dlls = os.path.join(PY_SOURCE, "DLLs")
    dst_dlls = os.path.join(PORTABLE_DIR, "DLLs")
    if os.path.exists(src_dlls) and not os.path.exists(dst_dlls):
        print("Copiando carpeta DLLs...")
        shutil.copytree(src_dlls, dst_dlls)
    print("[2/4] DLLs internas copiadas.")

    # 3. Copiar carpeta Lib base (excluyendo tests para ahorrar espacio)
    src_lib = os.path.join(PY_SOURCE, "Lib")
    dst_lib = os.path.join(PORTABLE_DIR, "Lib")
    if os.path.exists(src_lib) and not os.path.exists(dst_lib):
        print("Copiando biblioteca estándar Lib...")
        shutil.copytree(
            src_lib, dst_lib,
            ignore=shutil.ignore_patterns("test", "tests", "idlelib", "tcl*")
        )
    print("[3/4] Biblioteca estándar copiada.")

    # 4. Copiar librerías de terceros (site-packages de usuario)
    dst_site = os.path.join(dst_lib, "site-packages")
    os.makedirs(dst_site, exist_ok=True)
    if os.path.exists(USER_SITE):
        print("Copiando paquetes instalados (flask, faster-whisper, pandas, etc.)...")
        for item in os.listdir(USER_SITE):
            if item in ["__pycache__"]:
                continue
            s_item = os.path.join(USER_SITE, item)
            d_item = os.path.join(dst_site, item)
            if not os.path.exists(d_item):
                try:
                    if os.path.isdir(s_item):
                        shutil.copytree(s_item, d_item)
                    else:
                        shutil.copy2(s_item, d_item)
                except Exception as e:
                    print(f"Aviso al copiar {item}: {e}")
    print("[4/4] Paquetes de ofimática y modelos integrados en site-packages.")

    # 5. Configurar archivo ._pth para forzar rutas relativas y aislamiento total
    pth_content = (
        ".\n"
        "Lib\n"
        "Lib\\site-packages\n"
        "DLLs\n"
        "import site\n"
    )
    with open(os.path.join(PORTABLE_DIR, "python314._pth"), "w", encoding="utf-8") as f:
        f.write(pth_content)

    print("\n[ÉXITO TOTAL] Entorno Python portable ensamblado con éxito.")
    print(f"Ubicación: {os.path.join(PORTABLE_DIR, 'python.exe')}")

if __name__ == "__main__":
    construir()
