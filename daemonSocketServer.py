import socket
import threading

global addresses
addresses = []

def startDaemonSocket(port, byteSize, maxConnections):
    # get the hostname
    host = socket.gethostname()
    '''serverSocket = socket.socket()  # get instance

    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind((host, port))  # bind host address and port together
    serverSocket.listen(maxConnections)
    
    conn, address = serverSocket.accept()  # accept new connection

    print("Connection from: " + str(address))
'''
    for c in range(maxConnections):
        print(c)
        localSocket = socket.socket()
        localSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        localSocket.bind((host, port))  # bind host address and port together
        localSocket.listen(15)
        conn, target = localSocket.accept()

        print(f"Connection from: {target}")

        conThread = threading.Thread(target=socketIngestData, args=(conn, target, byteSize))
        conThread.start()
        pass



def socketIngestData(con, target, bytes):
    addresses.append(target)
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
           print(f"Doradcasting {a} to {message}")
           sock.send(message.encode())
           sock.close()
