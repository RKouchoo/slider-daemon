# https server for client daemon comms


import time
import http.server


def startServer(port, path, fileName):
	# run the server for the latest image
	return False 