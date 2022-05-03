from netTools import *

def simpleClient(location):

    client = socket(AF_INET, SOCK_STREAM)
    client.connect((location, 2024))
    outgoing = "JOIN chatroom1 Rubin"
    client.send(outgoing.encode('ascii'))
    # msg = client.recv(1024)
    # response = msg.decode('ascii')
    # print(response)

    client.close()

simpleClient("172.16.219.84")
