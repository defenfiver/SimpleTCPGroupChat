from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR


def handleClient(sock):
    # Handle communication with one client
    sock.send(b"Enter your name")
    name = sock.recv(1024)  # Receive the name from the client
    clients[sock] = name
    name = str(name)
    sock.send(b"Client connected")
    print(f"Client connected: {name}")
    print(f"All connected clients: {clients}")
    # Remember to close the socket when done
    sock.close()

def accepts():
    while True:
        connection_socket, tmp = server_socket.accept()
        print("User connected")
        connection_socket.send("Hi".encode())
        Thread(target=handleClient, args=(connection_socket,))
        

clients = {}
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(("", 5000))
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

    