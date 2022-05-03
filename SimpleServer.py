from socket import *
import threading
from threading import *

sockets = []

import atexit

def exit_handler():
    with open("chatrooms.txt", 'w'):
        print("Wiped chatrooms")

atexit.register(exit_handler)

def simpleServer():
    serversocket = socket(AF_INET, SOCK_STREAM)
    serversocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    IP_address = getIPAddress()
    serversocket.bind((IP_address, 2025))

    myLock = Lock()

    while True:
        serversocket.listen(1)
        print("Listening on " + IP_address)
        print("Waiting for connection...")
        clientsocket, addr = serversocket.accept()
        sockets.append((clientsocket,addr))

        try:
            threading.Thread(target=processRequest, args=(clientsocket, addr, myLock)).start()
        except:
            pass
    serversocket.close()

def processRequest(clientsocket, addr, lock):
    join_cmd = str(receiveMessage(clientsocket.recv(1024)))
    parts = join_cmd.split()
    if "JOIN" in join_cmd and len(parts) == 3:
        chat_room_name = parts[1]
        user_name = parts[2]
        chatrooms = getChatrooms()
        if '' in chatrooms.keys():
            chatrooms.pop('')
        if chat_room_name not in chatrooms.keys():
            chatrooms[chat_room_name] = [[user_name, addr[0]]]
            sendMessage("Ok, \t" + chat_room_name + " created", clientsocket)
        else:
            for user in chatrooms[chat_room_name]:
                if user_name in user[0]:
                    sendMessage("Denied \t username not unique", clientsocket)
                    clientsocket.close()
                    return None
            if chat_room_name in chatrooms.keys():
                sendMessage("Ok \t joined " + chat_room_name, clientsocket)
                chatrooms[chat_room_name].append([user_name, addr[0]])

        lock.acquire()
        updateChatrooms(chatrooms)
        lock.release()

        while True:
            message = receiveMessage(clientsocket.recv(1024))
            if message[:4] == "SEND":
                send_to_chat(user_name, message[5:], chat_room_name)
            elif message == "WHO":
                members = ""
                chatrooms = getChatrooms()
                for i in chatrooms[chat_room_name]:
                    members += i[0] + " "
                sendMessage("MEMBERS \t" + members, clientsocket)
            elif message == "LIST":
                list_of_rooms = ""
                for i in chatrooms.keys():
                    list_of_rooms += i + " "
                sendMessage("ROOMS \t" + list_of_rooms, clientsocket)
            elif message == "EXIT":
                for i in chatrooms[chat_room_name]:
                    if user_name == i[0]:
                        lock.acquire()
                        chatrooms[chat_room_name].remove(i)
                        lock.release()
                for i in sockets:
                    if addr == i[1]:
                        lock.acquire()
                        sockets.remove(i)
                        lock.release()
                lock.acquire()
                updateChatrooms(chatrooms)
                lock.release()
                send_to_chat(user_name, user_name + " left the chat", chat_room_name)

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
                file.write(user[0] + "," + user[1] + " ")
            file.write("\n")

def send_to_chat(user_name, message, chat_room_name):
    rooms = getChatrooms()
    count = 0
    for user in rooms[chat_room_name]:
        ip = user[1]
        print("user" + str(count) + " ip: " + ip)
        count += 1
        global sockets
        for client in sockets:
            print("\t" + client[1][0])
            if ip == client[1][0]:
                sendMessage(user_name + ": " + message, client[0])
                print("Sent "+ user_name + ": " + message + " to " + client[1][0] + " in " + chat_room_name)


simpleServer()


