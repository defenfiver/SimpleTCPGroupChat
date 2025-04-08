from threading import Thread
from socket import socket

def handleClient(sock):
  # Handle communication with one client

  # Remember to close the socket when done
  sock.close()

server_socket = '__'
server_socket.listen(5000)
while some_condition_to_check_here:
  connection_socket, _ = server_socket.accept()
  t = Thread(target = handleClient, args=(connection_socket,))
  t.start()
server_socket.close()