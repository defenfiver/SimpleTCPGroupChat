from ast import Try
from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from xmlrpc import server


def handleClient(sock):
    """
    Handles the connection between the server and one client

    sock: the socket used for the client 
    """
    try: 
        name = sock.recv(1024).decode()  # Receive the name from the client
    except ConnectionResetError:  # Happens when the client is closed 
        sock.close()
        print("[Server Error]: Client closed before name was entered")
        return
    clients[sock] = name  # Adds to the client dictionary, to be able to store in between threads
    name = str(name)
    sendClients(f'[Server]: {name} has connected'.encode())  
    data = f'[Server]: Currently Connected: {getAllClients()}'  
    sock.send(data.encode())  # Sends Currently Connected Message to only the user who is newly connecting
    print(f'{data} (Only sent to {name})')  # Prints the messsage to the server console
    while True:  # Always active, as it ends when the user closes their client
        try:
            data = sock.recv(1024).decode()
        except ConnectionResetError:  # Happens when the client is closed 
            clients.pop(sock)
            sendClients(f'[Server]: {name} has disconnected'.encode())
            sendClients(f"[Server]: Users remaining: {getAllClients()}".encode())
            sock.close()
            return
        sendClients(f'[{name}]: {data}'.encode())  # Sends the message sent from one user to ever client currently connected


def getAllClients() -> str:
    """
    returns the names of all users connected to the server as a string
    """
    if not clients.keys():  # If no one is connected
        return ""
    nameList = []
    for x in clients:  # Creates a list of names of the users 
        nameList.append(clients[x])
    names = nameList.pop(0)
    for x in nameList:
        names += f', {x}'
    return names

def sendClients(message):
    """
    Sends a message to every client connected to the network, and prints in to the server's console

    message: the message to be sent to every client
    """
    for x in clients:
        x.send(message)
    print(f'{message.decode()}')

def accepts():
    """
    Accepts all connection to the server's socket and creates a thread to handle each connection asynchronously
    """
    while running:
        try: 
            connection_socket, tmp = server_socket.accept()
            Thread(target=handleClient, args=(connection_socket,)).start()
        except OSError:
            return

def main():
    try:
        while True:  # Creates a thread to accept all of the client connections
            acceptThread = Thread(target = accepts)
            acceptThread.start()
            while True:
                userInput = input("Type stop to stop")
                if userInput.lower() in ["quit", "stop", "end", "exit"]:
                    running = False
                    server_socket.close()
                    print("Server closed")
                    return
    except KeyboardInterrupt:
        server_socket.close()
        print("Server closed due to KeyboardInterrupt")


if __name__ == "__main__":
    clients = {}  # A dictionary of client sockets and the names attached to them, sockets being the unique key
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(("", 801))
    server_socket.listen(4)
    global running
    running = True
    main()

    
    

    

    