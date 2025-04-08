from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR


def handleClient(sock):
    # Handle communication with one client
    socket.send("Hi")
    # Remember to close the socket when done
    sock.close()

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(("", 5000))
server_socket.listen(4)
while True:
    connection_socket, _ = server_socket.accept()
    t = Thread(target = handleClient, args=(connection_socket,))
    t.start()
    hi = input("type anything to quit")
    if not hi:
        server_socket.close()