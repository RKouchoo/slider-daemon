# script that executes the latest download

import os
import glob
import subprocess
import datetime
import time
from datetime import timezone, datetime

def work(timeWaitMins, sattelite, resLevel, socketPort):
    os.chdir("./image")

    sliderArgs = [
        "./slider-cli",
        f"--satellite={sattelite}",
        "--sector=full-disk",
        "--product=geocolor",
        "-i",
        "1",
        "-z",
        f"{resLevel}",
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
        if (os.path.isfile(os.getcwd() + "/image/latest.png")):
            os.rename(f"{os.getcwd()}/image/latest.png",  f"{os.getcwd()}/image/{str(now)}_previous.png")

        for file in glob.glob("cira*.png"):
            os.rename(file, "latest.png")

        # wait x mins for the next image to come avaliable
        print(f"Gathered latest image, daemon sleeping for: {timeWaitMins}min")


        time.sleep(timeWaitMins * 60)

