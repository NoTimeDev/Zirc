import subprocess
import sys
import os
import platform
import shutil

def Update(Ver): 

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
            drive = os.getcwd()[:os.getcwd().find(":")]
            os.chdir(drive + ":/")

        fet = subprocess.run(["git", "clone", "https://github.com/NoTimeDev/Zirc"], capture_output=True, text=True)

        if platform.system() == "Linux":
            os.chdir(os.path.expanduser("~/Zirc"))
        elif platform.system() == "Windows":
            drive = os.getcwd()[:os.getcwd().find(":")]
            os.chdir(drive + ":/Zirc")
        
        with open("LV.txt", "r") as File:
            NewVer = File.read()


        IsNewVer = NewVer != Ver

        if IsNewVer == True:
            if platform.system() == "Linux":
                subprocess.run(["python3", "Build.py"])
            elif platform.system() == "Windows":
                subprocess.run(["python", "Build.py"])
            os.chdir("..")
            shutil.rmtree("./Zirc")
        else:
            print(f"On the latest version of zirc verison {Ver}")
            os.chdir("..")
            shutil.rmtree("./Zirc")
