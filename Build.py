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

elif platform.system() == "Windows":
    import time

    print("Getting pyinstaller..")
    result = subprocess.run(["pip", "install", "pyinstaller", "--break-system-packages"], capture_output=True, text=True)
    subprocess.run(["pip", "install", "psutil"])

    print("Building Main.py")
    result = subprocess.run(["pyinstaller",  "--onefile", "Main.py", "-n", "zirc"], capture_output=True, text=True)

    if os.path.isdir(r"C:\Zedcomp") == False:
        os.mkdir(r"C:\Zedcomp")


    subprocess.Popen([sys.executable, "Buildfn.py"])
    time.sleep(3)
    os._exit(0)

else:
    print("Unsupported OS", file=sys.stderr)
    exit(1)
