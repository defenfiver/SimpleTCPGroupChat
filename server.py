from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR


def handleClient(sock):
    # Handle communication with one client
    #sock.send("Server: Enter your name".encode())
    name = sock.recv(1024).decode()  # Receive the name from the client
    clients[sock] = name
    name = str(name)
    print(f"Client connected: {name}")
    names = ""
    for x in clients:
        names = f'{names}, {clients[x]}'
    print(f"All connected clients: {names}")
    while True:
        data = sock.recv(1024).decode()
        data = f'{name}: {data}'
        sendClients(data)

def sendClients(message):
    for x in clients:
        x.send(message.encode())

def accepts():
    while True:
        connection_socket, tmp = server_socket.accept()
        print("User connected")
        Thread(target=handleClient, args=(connection_socket,)).start()
        

clients = {}
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(("", 801))
server_socket.listen(4)

try:
    while True:
        acceptThread = Thread(target = accepts)
        acceptThread.start()
        acceptThread.join()

except KeyboardInterrupt:
    print("Shutting Down Server")

finally:
   server_socket.close()
   print("Server closed")
    

server_socket.close()

    