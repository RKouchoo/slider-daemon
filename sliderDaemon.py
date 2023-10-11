# main daemon thread

import threading
import json 

import daemonWorker as daemon
import sliderServer as server
import daemonSocketServer as daemonSocket

socketByteSize = 1024
socketMaxConns = 4

config = []

# load the json config
with open("daemon.json", "r") as configFile:
    config = json.load(configFile)
    configFile.close()

imgPort = int(config["imgServerPort"])

# init and kick off services with the config
socketThread = threading.Thread(target=daemonSocket.startDaemonSocket, args=(int(config["socketServerPort"]), socketByteSize, socketMaxConns))
serverThread = threading.Thread(target=server.startImgServer, args=(imgPort,))

daemonThread = threading.Thread(target=daemon.work, args=(int(config["timeDelay"]), config["satellite"], int(config["resolutionLevel"]), int(config["socketServerPort"])))

socketThread.start()
serverThread.start()

daemonThread.start()
