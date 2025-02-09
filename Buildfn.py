import sys 
import subprocess
import psutil
import time
import shutil
import os

import psutil
print("l")
for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
    if proc.info['name'] == 'python.exe' and proc.info['cmdline'] and proc.info['cmdline'][1] == 'Build.py':
        proc.terminate()

        shutil.move(r".\dist\zirc.exe", r"C:\Zedcomp\zirc.exe")    
        
        shutil.rmtree(r".\dist")
        shutil.rmtree(r".\build")
        os.remove(r".\zirc.spec")

        os._exit(1)
    elif proc.info['name'] == 'python.exe' and proc.info['cmdline'] and proc.info['cmdline'][1] == 'Update.py':
        proc.terminate()

        shutil.move(r".\dist\zirc.exe", r"C:\Zedcomp\zirc.exe")    
        
        shutil.rmtree(r".\dist")
        shutil.rmtree(r".\build")
        os.remove(r".\zirc.spec")

        os.chdir("..")
        shutil.rmtree("./Zirc")

        os._exit(1)
