# client sided daemon

import os
import hashlib
import json
import glob
import requests
import time
import datetime
from datetime import timezone

import ctypes

socketByteSize = 1024
config = []


# load the json config
with open("client.json", "r") as configFile:
    config = json.load(configFile)
    configFile.close()


def gatherLatestImage(server, port, path):
    now = datetime.now(tz=timezone.utc).timestamp() * 1000

    if config["saveImageLocal"] == "true":
        for file in glob.glob(path):
            os.rename(file, f"{now}.png")
    else:
        os.remove(f"{path}\latest.png")

    latest = requests.get(server + f":{port}").content
    with open(f"{path}\latest.png", "wb") as handler:
        handler.write(latest)

    setLatestAsWallpaper(f"{path}\latest.png")


def getHashFromServer(server, port, path):
    latest = requests.get(server + f":{port}").content
    with open(f"{path}\hash.md5", "wb") as handler:
        handler.write(latest)

    return getCurrentSavedHash(clientMd5Path)


def getCurrentSavedHash(file):
    with open(file, "r") as md5File:
        config = json.load(md5File)
        return config["md5"]


def setLatestAsWallpaper(image):
    SPI_SETDESKWALLPAPER = 20 # tell the kernel we want to change wallpaper
    wallPos = 3 # what style, 3 is fit

    if config["os"] == "windows":
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image, wallPos) # invoke the kernel


def compareHashes(current, latest):
    if current == latest:
        return False
    else:
        return True



md5 = config["md5"]
clientMd5Path = f"{os.getcwd()}/image/{md5}"

while True:
    try:
        currentHash = getCurrentSavedHash(clientMd5Path) # load the current hash into memory
        latestHash = getHashFromServer(config["imgServerAdress"], config["hashServerPort"], os.path.abspath(config["md5"])) # grab the new hash from the server and save to disk
    except:
        print("Failed to get data from the server, sleeping for interval")
        time.sleep(int(config["checkIntervalMins"]) * 60)
        continue

    if compareHashes(currentHash, latestHash):
        gatherLatestImage(config["imgServerAdress"], config["imgServerPort"], os.path.abspath("image"))

    time.sleep(int(config["checkIntervalMins"]) * 60)