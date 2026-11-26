import os
import shutil
import sys

def get_dir_size(path):
    total = 0
    for root, dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(root, f)
            if os.path.exists(fp):
                total += os.path.getsize(fp)
    return total / (1024 * 1024)

py_base = r"C:\Python314"
user_site = os.path.expanduser(r"~\AppData\Roaming\Python\Python314\site-packages")

print(f"Base Python ({py_base}): {get_dir_size(py_base):.1f} MB")
if os.path.exists(user_site):
    print(f"User site-packages ({user_site}): {get_dir_size(user_site):.1f} MB")
