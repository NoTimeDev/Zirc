#This Script Can Be Uses To Turn Main.py into an excutable

import subprocess
import platform
import sys
import shutil
import os

if platform.system() == "Windows":

    try:
        res = subprocess.run(["pyinstaller"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except FileNotFoundError:
        result = subprocess.run(["pip", "install", "pyinstaller", "--break-system-packages"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print("pip may not be installed", file=sys.stderr)
            exit(1)
    
        stdout_output = result.stdout
        stderr_output = result.stderr
    
        print("Rerun the installer")
     
    else:
        res1 = subprocess.run(["pyinstaller", "--onefile", "Main.py", "--name", "zirc"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode == 1:
            print("Something went wrong")
            exit(1)
        else:
            src = "./dist/zirc"
            dest = "."
            shutil.move(src, dest)
            shutil.rmtree("./dist")
            shutil.rmtree("./build")
            os.remove("./zirc.spec")
            exit(0)
        

elif platform.system() == "Linux":
    pipm = input("Enter the name of your pip(eg pip-3, pip, python-pip-3): ")
    try:
        res = subprocess.run(["pyinstaller"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except FileNotFoundError:
        result = subprocess.run([pipm, "install", "pyinstaller", "--break-system-packages"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print("pip may not be installed", file=sys.stderr)
            exit(1)
    
        stdout_output = result.stdout
        stderr_output = result.stderr
    
        print("Rerun the installer")
     
    else:
        res1 = subprocess.run(["pyinstaller", "--onefile", "Main.py", "--name", "zirc"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode == 1:
            print("Something went wrong")
            exit(1)
        else: 
            src = "./dist/zirc"
            dest = "."
            shutil.move(src, dest)
            shutil.rmtree("./dist")
            shutil.rmtree("./build")
            os.remove("./zirc.spec")
            exit(0)
        

   


