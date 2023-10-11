# main daemon thread

import threading
import json 

import daemonWorker as daemon
import sliderServer as server

config = []

# load the json config
with open("daemon.json", "r") as configFile:
    config = json.load(configFile)
    configFile.close()

# init and kick off services with the config
daemonThread = threading.Thread(target=daemon.work, args=(int(config["timeDelay"]), config["satellite"], int(config["resolutionLevel"])))
serverThread = threading.Thread(target=server.startImgServer, args=(int(config["imgServerPort"])))

daemonThread.start()
serverThread.start()