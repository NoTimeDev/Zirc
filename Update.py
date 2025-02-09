import subprocess
import sys
import os
import platform
import shutil

def Update(): 
    Ver = "0.2"

    try:
        subprocess.run(["git"], capture_output=True, text=True)     
    except FileNotFoundError:
        print("Git is not found installing it, please confirm any inputs")
        if platform.system() == "Windows":
            print("Try running \"winget install GIT.GIT\"")
        sys.exit(1)

    else:
        if platform.system() == "Linux":
            os.chdir(os.path.expanduser("~"))
        elif platform.system() == "Windows":
            os.chdir("C:/")

        fet = subprocess.run(["git", "clone", "https://github.com/NoTimeDev/Zirc"], capture_output=True, text=True)

        if platform.system() == "Linux":
            os.chdir(os.path.expanduser("~/Zirc"))
        elif platform.system() == "Windows":
            os.chdir("C:/Zirc")
        
        with open("LV.txt", "r") as File:
            NewVer = File.read()


        IsNewVer = NewVer[:-1] != Ver
        
        if IsNewVer == True:
            if platform.system() == "Linux":
                subprocess.run(["python3", "Build.py"])
            elif platform.system() == "Windows":
                subprocess.run(["python", "Build.py"])
        else:
            print("Latest version of zirc")
        os.chdir("..")
        shutil.rmtree("./Zirc")
        
Update()