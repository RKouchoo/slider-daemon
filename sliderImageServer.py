# https server for client daemon comms

import os
import http.server
import socketserver
import socket

imgPath = os.getcwd() + "/image/latest.png"

def startImgServer(port):
    with socketserver.TCPServer(("", int(port)), http.server.SimpleHTTPRequestHandler) as httpd:
        # Override the handler's translate_path method to serve a specific file
        httpd.allow_reuse_address = False
        httpd.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        httpd.RequestHandlerClass.translate_path = lambda self, path: imgPath
        print(f"Serving image {imgPath} at port {port}")
        httpd.serve_forever()