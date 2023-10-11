import socket

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

        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(byteSize).decode()
        if not data:
            conn.close()
            # if data is not received break
            break

    conn.close()  
