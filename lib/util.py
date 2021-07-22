import os

import lib.settings as settings

def fileExist(fileName):
    return os.path.exists(settings.pwd + fileName)

def loadConfig():
    if not fileExist("/lib/config"):
        createConfig()
    else:
        load = []
        with open(settings.pwd + "/lib/config", 'r') as file:
            for line in file:
                load.append(line)
        if len(load) == 0 or load[0] != "EN" and load[0] != "FR" \
       and load[1] != True and load[1] != False \
       and load[2] not in ["VS", "S", "N", "L", "VL", "I"]:
            print("Config error: Fixing...")
            createConfig()
        else:
            settings.lang = load[0]
            settings.oneSolution = load[1]
            settings.timeLimit = load[2]
            print("Settings loaded succesfully !")

def createConfig():
    with open(settings.pwd + "/lib/config", 'w') as file:
        file.write(f"EN\nTrue\nN")
        settings.lang = "EN"
        settings.oneSolution = True
        settings.timeLimit = "N"
        print("Config created.")
    