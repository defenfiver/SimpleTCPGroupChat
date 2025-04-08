from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR


def handleClient(sock):
    name = sock.recv(1024).decode()
    clients[sock] = name
    sock.send(f'Hi {name}!'.encode())
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
acceptThread = Thread(target = accepts)
acceptThread.start()
acceptThread.join()
server_socket.close()
print("socket closed")
    