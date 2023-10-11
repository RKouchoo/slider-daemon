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

def startDaemonSocket(port):
    # get the hostname
    host = socket.gethostname()
    server_socket = socket.socket()  # get instance

    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection

    print("Connection from: " + str(address))

    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break

    conn.close()  
