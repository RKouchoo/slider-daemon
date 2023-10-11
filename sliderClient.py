# client sided daemon

import os
import socket
import json 

config = []

# load the json config
with open("client.json", "r") as configFile:
    config = json.load(configFile)
    configFile.close()


def connectToServer(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    return client

def gatherLatestImage(server, path):
    latest = ""
    setLatestAsWallpaper(latest)
    # do something

def setLatestAsWallpaper(latest):
    # do something
    return


####



sock = connectToServer("localhost", 8001)

while True:
    # wait for data
    data = sock.recv(1024)
    if not data:
        break
    
    if data.decode("utf8") == "ready":
        gatherLatestImage("localhost", 8000)
        
