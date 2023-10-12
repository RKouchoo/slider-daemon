
import os
import http.server
import socketserver
import socket

hashPath = os.getcwd() + "/image/hash.md5"

def startHashServer(port):
    with socketserver.TCPServer(("", int(port)), http.server.SimpleHTTPRequestHandler) as httph:
        # Override the handler's translate_path method to serve a specific file
        httph.allow_reuse_address = False
        httph.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        httph.RequestHandlerClass.translate_path = lambda self, path: hashPath
        print(f"Serving hash {hashPath} at port {port}")
        httph.serve_forever()