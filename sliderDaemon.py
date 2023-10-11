# main daemon thread

import threading
import json 

import daemonWorker as daemon
import sliderServer as server

socketByteSize = 1024
socketMaxConns = 2 

config = []

# load the json config
with open("daemon.json", "r") as configFile:
    config = json.load(configFile)
    configFile.close()

# init and kick off services with the config
daemonThread = threading.Thread(target=daemon.work, args=(int(config["timeDelay"]), config["satellite"], int(config["resolutionLevel"], int(config["socketServerPort"]))))
serverThread = threading.Thread(target=server.startImgServer, args=(int(config["imgServerPort"])))
socketThread = threading.Thread(target=server.startDaemonSocket, args=(int(config["socketServerPort"], socketByteSize, socketMaxConns)))

daemonThread.start()
serverThread.start()
socketThread.start()