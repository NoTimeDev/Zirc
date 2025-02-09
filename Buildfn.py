import sys 
import subprocess
import psutil
import time
import shutil
import os

for proc in psutil.process_iter():
    try:
        if proc.name == "python.exe" and "Build.py" in proc.cmdline():
            proc.kill()

            time.sleep(2)
                
            shutil.move(r".\dist\zirc.exe", r"C:\Zedcomp\zirc.exe")    
        
            shutil.rmtree(r".\dist")
            shutil.rmtree(r".\build")
            os.remove(r".\zirc.spec")

            if os.getcwd()[1:] == ":/Zirc":
                os.chdir("..")
                shutil.rmtree("./Zirc")

    except:
        continue
