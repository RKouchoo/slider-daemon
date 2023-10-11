# client sided daemon

import os
import socket
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


def connectToServer(host, port):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
    except socket.error as e:
        print(e)
        return None  

    return client


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


def setLatestAsWallpaper(image):
    SPI_SETDESKWALLPAPER = 20 # tell the kernel we want to change wallpaper
    wallPos = 3 # what style, 3 is fit

    if config["os"] == "windows":
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image, wallPos) # invoke the kernel
add = config["imgServerAdress"]
while True:
    sock = connectToServer(config["imgServerAdress"], int(config["socketServerPort"]))

    # catch a broken link, attempt to reconnect
    if not sock:
        print("Server connection failed, retry in 15s")
        time.sleep(15) # wait 15 sec then try again
        continue
    print(f"connected to host: {add}")

    # wait for data
    data = sock.recv(socketByteSize)
    if not data:
        continue

    print(data.decode("utf8")) # debug
    if data.decode("utf8") == "ok":
        gatherLatestImage(config["imgServerAdress"], config["imgServerPort"], os.path.abspath("image"))
    else:
        pass
        
