from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

# define a dictionary to store the connection socket and the client name
clients = {}
# define a dictionary to store the connection socket and the client address
addresses = {}

HOST = '127.0.0.1'
PORT = 33008
BUFSIZ = 1024
# address tuple containing connection address and port number
ADDR = (HOST, PORT)
# create a socket
SERVER = socket(AF_INET, SOCK_STREAM)
# associate the socket with the server address and port
SERVER.bind(ADDR)


# accept connections from clients
def accept_incoming_connections():
    '''
    The return value is a pair (connection_socket, client_address) where connection_socket 
    is a new socket object usable to send and receive data on the connection, 
    and client_address is the address bound to the socket on the other end of the connection.
    So we basically have one listening socket active while the server is running and one 
    new connected socket for each accepted connection which is active until the connection is closed.
    '''
    # wait infinitely for new connections
    while True:
        # accept the client request
        client, client_address = SERVER.accept()
        print("{} has connected".format(client_address))
        client.send(bytes("Hello there!Please enter your name!", "utf8"))
        # add the client address to the addresses dictionary
        addresses[client] = client_address
        # handle the client
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):
    # get the name of the client
    name = client.recv(BUFSIZ).decode("utf8")
    # prepare a welcome message to the client
    welcome = "Welcome {}!To exit please close the window".format(name)
    # send the welcome message to the client
    client.send(bytes(welcome, "utf-8"))
    # prepare a group message
    message = "{} has joined the chat".format(name)
    # broadcast the group message to everybody
    broadcast(bytes(message, "utf8"))
    # add the client to the clients dictionary
    clients[client] = name
    # keep listening for messages
    while True:
        # get the message from the client
        message = client.recv(BUFSIZ)
        # if message does not contain 'quit'
        if message != bytes("quit", "utf8"):
            # broadcast the message to everyone
            broadcast(message, name + ":")
        else:
            # confirm the client you received a 'quit' message
            client.send(bytes("quit", "utf8"))
            # close the socket connection
            client.close()
            # delete the client entry from the clients dictionary
            del clients[client]
            # broadcast everyone that the client has left
            broadcast(bytes("{} has left the chat".format(name), "utf8"))
            break


def broadcast(message, prefix=""):
    # prefix gives the name of the person who sent the message
    # broadcast message to everyone
    for socket in clients:
        socket.send(bytes(prefix, "utf8") + message)


if __name__ == "__main__":
    # listen for 5 connections at max
    SERVER.listen(5)
    print("Waiting for connection")
    # create a thread to accept connection
    accept_thread = Thread(target=accept_incoming_connections)
    # start the thread
    accept_thread.start()
    # wait until the thread has finished executing
    accept_thread.join()
    # close the server
    SERVER.close()
