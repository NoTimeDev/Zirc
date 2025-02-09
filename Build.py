import os
import platform
import subprocess
import sys
import shutil

if platform.system() == "Linux":
    print("Getting pyinstaller..")
    result = subprocess.run(["pip3", "install", "pyinstaller", "--break-system-packages"], capture_output=True, text=True)
        

    print("Building Main.py")
    result = subprocess.run(["pyinstaller",  "--onefile", "Main.py", "-n", "zirc"], capture_output=True, text=True)
    
    
    print("Adding zirc to bin")
    shutil.move("./dist/zirc", "/usr/local/bin/zirc")
    
    
    shutil.rmtree("./dist")
    shutil.rmtree("./build")
    os.remove("./zirc.spec")

    print("Building Update.py")
    result = subprocess.run(["pyinstaller",  "--onefile", "Update.py", "-n", "zircupd"], capture_output=True, text=True)
    
    
    print("Adding zirc to bin")
    shutil.move("./dist/zircupd", "/usr/local/bin/zircupd")
    
    
    shutil.rmtree("./dist")
    shutil.rmtree("./build")
    os.remove("./zircupd.spec")

elif platform.system() == "Windows":
    print("Getting pyinstaller..")
    result = subprocess.run(["pip", "install", "pyinstaller", "--break-system-packages"], capture_output=True, text=True)
        

    print("Building Main.py")
    result = subprocess.run(["pyinstaller",  "--onefile", "Main.py", "-n", "zirc"], capture_output=True, text=True)

    if os.path.isdir(r"C:\Zedcomp") == False:
        os.mkdir(r"C:\Zedcomp")

    shutil.move(r".\dist\zirc.exe", r"C:\Zedcomp\zirc.exe")    
        
    shutil.rmtree(r".\dist")
    shutil.rmtree(r".\build")
    os.remove(r".\zirc.spec")

    print("Building Update.py")
    result = subprocess.run(["pyinstaller",  "--onefile", "Update.py", "-n", "zircupd"], capture_output=True, text=True)

    if os.path.isdir(r"C:\Zedcomp") == False:
        os.mkdir(r"C:\Zedcomp")

    shutil.move(r".\dist\zircupd.exe", r"C:\Zedcomp\zircupd.exe")    
        
    shutil.rmtree(r".\dist")
    shutil.rmtree(r".\build")
    os.remove(r".\zircupd.spec")
else:
    print("Unsupported OS", file=sys.stderr)
    exit(1)
