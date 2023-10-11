# https server for client daemon comms

import os
import http.server
import socketserver
import socket

fileName = "latest.png"

def startImgServer(port):
	os.chdir("image")

	with socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler) as httpd:
		# Override the handler's translate_path method to serve a specific file
		httpd.RequestHandlerClass.translate_path = lambda self, path: fileName
		print(f"Serving {fileName} at port {port}")
		httpd.serve_forever()


def startDaemonSocket(port, byteSize, maxConnections):
    # get the hostname
    host = socket.gethostname()
    serverSocket = socket.socket()  # get instance

    # look
    serverSocket.bind((host, port))  # bind host address and port together
    serverSocket.listen(maxConnections)
    
    conn, address = serverSocket.accept()  # accept new connection

    print("Connection from: " + str(address))

    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(byteSize).decode()
        if not data:
            # if data is not received break
            break
    conn.close()  


def setReadyAck(ready):
      pass