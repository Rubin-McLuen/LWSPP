from socket import *
import threading
from threading import *

def simpleServer():
    serversocket = socket(AF_INET, SOCK_STREAM)
    serversocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    IP_address = getIPAddress()
    serversocket.bind((IP_address, 2024))


    while True:
        serversocket.listen(1)
        print("Listening on " + IP_address)
        print("Waiting for connection...")
        clientsocket, addr = serversocket.accept()
        try:
            threading.Thread(target=processRequest, args=(clientsocket, addr)).start()
        except:
            pass
    serversocket.close()

def processRequest(clientsocket, addr):
    cmd = receiveMessage(clientsocket.recv(1024))

def getIPAddress():
    s = socket(AF_INET, SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def sendMessage(message, clientsocket):
    clientsocket.send(message.encode('ascii'))
    print("Server: " + message)

def receiveMessage(response):
    message = response.decode('ascii')
    print("\tClient: " + message)
    return message

simpleServer()


