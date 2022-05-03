from netTools import *

def simpleClient(location):

    client = socket(AF_INET, SOCK_STREAM)
    client.connect((location, 2025))
    outgoing = "JOIN chatroom3 Tom"
    client.send(outgoing.encode('ascii'))
    while True:
        msg = client.recv(1024)
        response = msg.decode('ascii')
        print(response)
        outgoing = input()
        client.send(outgoing.encode('ascii'))
        if outgoing == "exit":
            break

    client.close()

simpleClient("172.16.219.84")
