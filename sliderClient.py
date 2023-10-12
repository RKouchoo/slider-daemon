# client sided daemon

import os
import json
import requests
import time
import datetime
from datetime import timezone, datetime

import ctypes

socketByteSize = 1024
config = []


# load the json config
with open("client.json", "r") as configFile:
    config = json.load(configFile)
    configFile.close()


def gatherLatestImage(server, port, path, newHash, oldHash):
    now = datetime.now(tz=timezone.utc).timestamp() * 1000
    latest = requests.get(f"http://{server}:{port}/latest.png").content

    if config["saveImageLocal"] == "true":
        os.rename(f"{path}\latest.png", f"{path}\{now}.png")
        print(f"Image caching enabled, saved previous image as {path}\{now}.png")
    else:
        os.remove(f"{path}\latest.png")

    with open(f"{path}\latest.png", "wb") as handler:
        handler.write(latest)

    setLatestAsWallpaper(f"{path}\latest.png")

    # update the hash file now
    with open(newHash, "r") as md5File:
        hashC = json.load(md5File)
        with open(oldHash, "w") as newmd5File:
            json.dump(hashC, newmd5File)
            newmd5File.close()
        md5File.close()


def getHashFromServer(server, port, path):
    latest = requests.get(f"http://{server}:{port}/hash.md5").content

    with open(path, "wb") as handler:
        #print(latest)
        handler.write(latest)

    return getCurrentSavedHash(path)


def getCurrentSavedHash(file):
    with open(file, "r") as md5File:
        hashC = json.load(md5File)
        return hashC["md5"]


def setLatestAsWallpaper(image):
    SPI_SETDESKWALLPAPER = 20 # tell the kernel we want to change wallpaper
    wallPos = 1 # what style, 3 is fit

    if config["os"] == "windows":
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image, wallPos) # invoke the kernel


def compareHashes(current, latest):
    print("Checking if server has update")
    if current == latest:
        print(f"No update yet, hashes match {current} : {latest} - retry in 1 min")
        return False
    else:
        print(f"New image!, hashes mismatch {current} : {latest}")
        return True


md5 = config["md5"]
clientMd5Path = f"{os.getcwd()}\\image\\{md5}"
clientTempMd5Path = f"{os.getcwd()}\\image\\temp.md5"

while True:
    try:
        currentHash = getCurrentSavedHash(clientMd5Path) # load the current hash into memory
        latestHash = getHashFromServer(config["imgServerAdress"], config["hashServerPort"], clientTempMd5Path) # grab the new hash from the server and save to disk

        if compareHashes(currentHash, latestHash):
            gatherLatestImage(config["imgServerAdress"], config["imgServerPort"], os.path.abspath("image"), clientTempMd5Path, clientMd5Path)
    
    except Exception as e:
        print(e)
        print("Failed to get data from the server, sleeping for interval")
        time.sleep(int(config["checkIntervalMins"]) * 60)
        continue

    time.sleep(int(config["checkIntervalMins"]) * 60)