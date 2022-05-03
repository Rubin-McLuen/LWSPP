from socket import *

def simpleServer():
    #create a socket object
    #   socket is a function that returns a variable of type socket (a constructor)
    #   AF_INET is the Address Format:Internet -- you are going to connect with an IP Address
    #   SOCK_STREAM it the type of socket --- how to package the data.
    serversocket = socket(AF_INET, SOCK_STREAM)

    #allow your server to reuse the address instead of waiting for a timeout
    serversocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    #Be sure that your socket communicates on it's IP address, on a specific port
    #   The port is 2000 -- this was chosen somewhat randomly
    #   NOTE: bind takes a tuple, not two parameters.
    
    serversocket.bind(("192.168.1.37", 2000))

    #Start listening for requests.
    #   Argument is the size of the request buffer
    serversocket.listen(1)

    #Block here until there is a request
    #   when you accept, you should know 2 values
    #   clientsocket and addr (who connected to you)
    print("Waiting for connection....")
    clientsocket,addr = serversocket.accept()
    print ("Connnection from", addr)

    #Send some information back to the client -
    #You don't know that another Python program connected,
    # so you have to convert your string to ASCII

    clientsocket.send(gethostname().encode('ascii'))
    clientsocket.close()
    serversocket.close()


simpleServer()


