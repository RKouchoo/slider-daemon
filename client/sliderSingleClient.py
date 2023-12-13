# script that executes the latest download

import os
import glob
import subprocess
import datetime
import time
from datetime import timezone, datetime
import schedule
import json


# load the config file 
with open("settings.json", "r") as configFile:
    config = json.load(configFile)
    configFile.close()

os.chdir("./images")

sliderArgs = [
    "./slider-cli",
    f"--satellite={config['satellite']}",
    "--sector=full-disk",
    "--product=geocolor",
    "-i",
    "1",
    "-z",
    f"{config['resolution']}",
    #"-v", # verbose for debug
    "-f",
    "png"
]

def setLatestImageBG():
    command = "gsettings set org.cinnamon.desktop.background picture-uri"
    image = "file://%s" % os.path.abspath("latest.png")

    try:
        os.system('%s "%s"' % (command, image))
    except IOError:
        print ("Error applying background!")
    
    print("set latest image as background!")


def run():
    # download the image using slider cli
    procState = subprocess.call(sliderArgs)
    print("Gathered latest image")
    # rename the old image with the current timestamp
    now = int(datetime.now(tz=timezone.utc).timestamp() * 1000)
    if (os.path.isfile(os.getcwd() + "/latest.png")):
        os.rename(f"{os.getcwd()}/latest.png",  f"{os.getcwd()}/{str(now)}_previous.png")

    for file in glob.glob("cira*.png"):
        os.rename(file, "latest.png")

    setLatestImageBG()


schedule.every(int(config['timeWaitMins'])).minutes.do(run)
# run main method first
run()


while True:
    schedule.run_pending()
    time.sleep(1)