# script that executes the latest download

import os
import glob
import subprocess
import datetime
from datetime import timezone
import time
import socket

isOkImage = "ok"
isNotOkImage = "no"

def connectToSockDaemonServer(host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    return client

def sendImageOkay(sock, isOk):
    sock.send(isOk.encode())

def work(timeWaitMins, sattelite, resLevel, socketPort):
    conn = connectToSockDaemonServer(socket.gethostname(), socketPort)

    os.chdir("./image")

    sliderArgs = [
        "./slider-cli",
        "--satellite=" + sattelite,
        "--sector=full-disk",
        "--product=geocolor",
        "-i",
        "1",
        "-z",
        str(resLevel),
        #"-v", # verbose for debug
		"-f",
        "png"
    ]

    # main loop, download the image and move + rename for the webserver
    while (True):
        # download the image using slider cli
        state = subprocess.call(sliderArgs)

        # rename the old image with the current timestamp (yes they are offset by 10 mins)
        now = int(datetime.now(tz=timezone.utc).timestamp() * 1000)
        if (os.path.isfile("latest.png")):
            os.rename("latest.png", str(now) + "_previous.png")

        for file in glob.glob("cira*.png"):
            os.rename(file, "latest.png")

        sendImageOkay(conn, isOkImage)
        time.sleep(5) # sleep for 5 sec, incase of network lag
        sendImageOkay(conn, isNotOkImage)

        # wait x mins for the next image to come avaliable
        print("Gathered latest image, daemon sleeping for: " + str(timeWaitMins))


        time.sleep(timeWaitMins * 60)

