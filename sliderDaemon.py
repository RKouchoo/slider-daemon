# main daemon thread

import threading
import json 

import daemonWorker as daemon
import sliderServer as server
#import daemonSocketServer as daemonSocket

socketByteSize = 1024
socketMaxConns = 4

config = []

# load the json config
with open("daemon.json", "r") as configFile:
    config = json.load(configFile)
    configFile.close()

imgPort = int(config["imgServerPort"])
hashPort = int(config["hashServerPort"])

serverThread = threading.Thread(target=server.startImgServer, args=(imgPort,))
hashThread = threading.Thread(target=server.startHashServer, args=(hashPort,))
daemonThread = threading.Thread(target=daemon.work, args=(int(config["timeDelay"]), config["satellite"], int(config["resolutionLevel"]), int(config["hashServerPort"])))

serverThread.start()
hashThread.start()

daemonThread.start()
