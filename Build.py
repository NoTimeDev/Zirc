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
    print("Getting pyinstaller..")
    result = subprocess.run(["pip", "install", "pyinstaller", "--break-system-packages"], capture_output=True, text=True)
        

    print("Building Main.py")
    result = subprocess.run(["python", "-m", "pyinstaller",  "--onefile", "Main.py", "-n", "zirc"], capture_output=True, text=True)
    
    
    print("Adding zirc to path")
    if os.path.isdir(r"C:\Zedcomp") == False:
        os.mkdir(r"C:\Zedcomp")

    shutil.move(r".\dist\zirc", r"C:\Zedcomp")

    import winreg as reg

    new_path = r"C:\Zedcomp"

    key = reg.HKEY_CURRENT_USER 
    path_value_name = "Environment"
    path_name = "Path"  
    
    with reg.OpenKey(key, r"Environment", 0, reg.KEY_WRITE) as registry_key:
        current_path, _ = reg.QueryValueEx(registry_key, path_name)

        if new_path not in current_path:
            new_path_value = current_path + ";" + new_path

            reg.SetValueEx(registry_key, path_name, 0, reg.REG_EXPAND_SZ, new_path_value)

    
    shutil.rmtree(r".\dist")
    shutil.rmtree(r".\build")
    os.remove(r".\zirc.spec")

else:
    print("Unsupported OS", file=sys.stderr)
    exit(1)
