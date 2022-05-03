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
    join_cmd = str(receiveMessage(clientsocket.recv(1024)))
    parts = join_cmd.split()
    if "JOIN" in join_cmd and len(parts) == 3:
        chat_room_name = parts[1]
        user_name = parts[2]
        chatrooms = getChatrooms()
        if '' in chatrooms.keys():
            chatrooms.pop('')
        if chat_room_name not in chatrooms.keys():
            chatrooms[chat_room_name] = [[user_name, addr]]
            sendMessage("Ok, \t" + chat_room_name + " created", clientsocket)
        else:
            if user_name in chatrooms[chat_room_name]:
                sendMessage("Denied \t username not unique", clientsocket)
                clientsocket.close()
            elif chat_room_name in chatrooms.keys():
                sendMessage("Ok \t joined " + chat_room_name, clientsocket)
                chatrooms[chat_room_name].append([user_name, addr])
        updateChatrooms(chatrooms)





    else:
        clientsocket.close()

def getIPAddress():
    s = socket(AF_INET, SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def sendMessage(message, clientsocket):
    clientsocket.send(message.encode('ascii'))

def receiveMessage(response):
    message = response.decode('ascii')
    return message

def getChatrooms():
    chatrooms = {}
    with open("chatrooms.txt",'r') as data:
        for line in data:
            room = line.strip().split(" ")
            room_name = room[0]
            names = []
            for i in room[1:]:
                name, addr = i.split(",")
                names.append([name,addr])
            chatrooms[room_name] = names
    return chatrooms

def updateChatrooms(chatrooms):
    with open("chatrooms.txt", 'w') as file:
        for room in chatrooms:
            file.write(room + " ")
            for user in chatrooms[room]:
                file.write(user[0] + "," + user[1][0] + " ")
            file.write("\n")

simpleServer()


