# https server for client daemon comms

import os
import http.server
import socketserver

fileName = "latest.png"

def startServer(port):
	os.chdir("image")

	with socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler) as httpd:
		# Override the handler's translate_path method to serve a specific file
		httpd.RequestHandlerClass.translate_path = lambda self, path: fileName
		print(f"Serving {fileName} at port {port}")
		httpd.serve_forever()
