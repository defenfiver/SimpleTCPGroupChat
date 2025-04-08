from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

clients = []

def handleClient(sock):
    # Handle communication with one client
    sock.send(b"Enter your name")
    name = sock.recv(1024)  # Receive the name from the client
    clients.append(name)
    name = str(name)
    sock.send(b"Client connected")
    print(f"Client connected: {name}")
    print(f"All connected clients: {clients}")
    # Remember to close the socket when done
    sock.close()

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(("", 80))
server_socket.listen(4)

try:
  while True:
      connection_socket, _ = server_socket.accept()
      t = Thread(target = handleClient, args=(connection_socket,))
      t.start()

except KeyboardInterrupt:
  print("Shutting Down Server")

finally:
   server_socket.close()
    