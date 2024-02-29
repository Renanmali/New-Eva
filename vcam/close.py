import psutil
import os
cwd = os.getcwd()

for proc in psutil.process_iter(attrs=['cmdline', 'name']):
    if 'python' in proc.info['name'] and proc.info['cmdline'][1] == cwd+"/vcam.py":
        # pprint(proc.info['cmdline'])
        proc.kill()
        print("Killed 'vcam' process")

import SharedArray as sa
try:
    sa.delete("vcam")
    print("Freed shared memory 'vcam'")
except FileNotFoundError:
    print("Shared memory 'vcam' already free")

import shutil
if os.path.isdir('.lock'):
    shutil.rmtree('.lock')
    print("Removed lock folder")