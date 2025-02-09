import sys 
import subprocess
import psutil
import time
import shutil
import os

import psutil
print("l")
for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
    if proc.info['name'] == "zirc.exe":
        proc.termiate()

for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
    if proc.info['name'] == 'python.exe' and proc.info['cmdline'] and proc.info['cmdline'][1] == 'Build.py':
        proc.terminate()

        drive = os.getcwd()[:os.getcwd().find(":")]

        if os.path.exists(drive + ":\Zedcomp\zirc.exe"):
            os.remove(drive + ":\Zedcomp\zirc.exe")

        shutil.move(r".\dist\zirc.exe", drive + r":\Zedcomp\zirc.exe")    
        
        shutil.rmtree(r".\dist")
        shutil.rmtree(r".\build")
        os.remove(r".\zirc.spec")

        os._exit(1)
    elif proc.info['name'] == 'python.exe' and proc.info['cmdline'] and proc.info['cmdline'][1] == 'Update.py':
        proc.terminate()
    
        drive = os.getcwd()[:os.getcwd().find(":")]

        if os.path.exists(drive + ":\Zedcomp\zirc.exe"):
            os.remove(drive + ":\Zedcomp\zirc.exe")
        
        shutil.move(r".\dist\zirc.exe", drive + r":\Zedcomp\zirc.exe")    
        
        shutil.rmtree(r".\dist")
        shutil.rmtree(r".\build")
        os.remove(r".\zirc.spec")

        os.chdir("..")
        shutil.rmtree("./Zirc")

        os._exit(1)
