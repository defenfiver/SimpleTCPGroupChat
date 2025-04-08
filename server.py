from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR


def handleClient(sock):
    # Handle communication with one client
    try: 
        name = sock.recv(1024).decode()  # Receive the name from the client
    except ConnectionResetError:
        sock.close()
        print("[Server Error]: Client closed before name was entered")
        return
    clients[sock] = name
    name = str(name)
    sendClients(f'[Server]: {name} has connected'.encode())
    data = f'[Server]: Currently Connected: {getAllClients()}'
    sock.send(data.encode())
    print(f'{data} (Only sent to {name})')
    while True:
        try:
            data = sock.recv(1024).decode()
        except ConnectionResetError:
            clients.pop(sock)
            sendClients(f'[Server]: {name} has disconnected'.encode())
            sendClients(f"[Server]: Users remaining: {getAllClients()}".encode())
            sock.close()
            return
        sendClients(f'[{name}]: {data}'.encode())


def getAllClients():
    if not clients.keys():
        return ""
    nameList = []
    for x in clients:
        nameList.append(clients[x])
    names = nameList.pop(0)
    for x in nameList:
        names += f', {x}'
    return names

def sendClients(message):
    for x in clients:
        x.send(message)
    print(f'{message.decode()}')

def accepts():
    while True:
        connection_socket, tmp = server_socket.accept()
        Thread(target=handleClient, args=(connection_socket,)).start()


if __name__ == "__main__":
    global clients
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

    