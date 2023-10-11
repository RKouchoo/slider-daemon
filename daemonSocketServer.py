import socket
import threading

global addresses
addresses = []

def startDaemonSocket(port, byteSize, maxConnections):
    # get the hostname
    host = socket.gethostname()
    serverSocket = socket.socket()  # get instance

    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind((host, port))  # bind host address and port together
    serverSocket.listen(maxConnections)
    
    conn, address = serverSocket.accept()  # accept new connection

    print("Connection from: " + str(address))

    while True:
        conn, address = serverSocket.accept()
        conThread = threading.Thread(target=socketIngestData, args=(conn, address, byteSize))
        conThread.start()



def socketIngestData(con, host, bytes):
    addresses.append(host)
    while True:
        msg = con.recv(bytes).decode("utf-8")
        if not msg:
            msg = ""
            break
        else:
            print(msg)
            broadcastAllSockets(con, addresses, msg)
            pass


def broadcastAllSockets(sock, add, message):

    for a in add:
           sock.send(message.encode())
