I am going to build a chat application where any numbers of users can join in and chat with each other.This application works using sockets and no third party dependencies are required.

Let us first go through certain basics of networking

**Sockets**

Sockets are the endpoints of a bidirectional communications channel. Sockets may communicate within a process, between processes on the same machine, or between processes on different machines.It may be implemented over a number of different channel types such as TCP, UDP, and so on.The type of communications between the two endpoints, typically SOCK_STREAM for connection-oriented protocols and SOCK_DGRAM for connectionless protocols.

**Domain**

The family of protocols that is used as the transport mechanism. These values are constants such as AF_INET, PF_INET, PF_UNIX, PF_X25, and so on.We will be using TCP sockets for this purpose, and therefore we use AF_INET and SOCK_STREAM flags.

**Type**

The type of communications between the two endpoints, typically SOCK_STREAM for connection-oriented protocols and SOCK_DGRAM for connectionless protocols.

**Hostname**

The identifier of a network interface.A string, which can be a host name, a dotted-quad address, or an IPV4 or IPV6 address.

**Port**

A port is a way to identify a specific process to which an Internet or other network message is to be forwarded when it arrives at a server.Each server listens for clients calling on one or more ports.

Let us see the application in action.We can either run the server side code in our local computer or in a server in my case a VPS.Then the client file can be run in our local computers.So each connection request from the local computers goes to the server (we pass in the server IP address and port number) and then the server handles all the connection requests.

Here we are running the chat application locally but in can be run in multiple computers running the server side code in a VPS.Below is the screenshot when we first start the app.Here we have two users 'Souvik' and 'Ritam'.Initally it asks to enter our names.

![Alt text](https://github.com/Souvikray/Chat-Application/blob/master/screenshot1.png?raw=true "Optional Title")

Now the chat can be initiated.So we can see the other user (the one on the right side) is informed that a new user has joined the chat room.

![Alt text](https://github.com/Souvikray/Chat-Application/blob/master/screenshot2.png?raw=true "Optional Title")

Currently the two users are chatting with each other

![Alt text](https://github.com/Souvikray/Chat-Application/blob/master/screenshot3.png?raw=true "Optional Title")

Now to exit the chat, we simply close the wondow.So here 'Ritam' (the user on the left) left the chat.So the other user 'Souvik' is informed about it.


![Alt text](https://github.com/Souvikray/Chat-Application/blob/master/screenshot4.png?raw=true "Optional Title")

Since we have added database support, so when the conversation is ended and next time the conversion starts, it retrieves the previous chat history.

![Alt text](https://github.com/Souvikray/Chat-Application/blob/master/screenshot5.png?raw=true "Optional Title")

The users can pick up from where they left when they restart the application.

![Alt text](https://github.com/Souvikray/Chat-Application/blob/master/screenshot6.png?raw=true "Optional Title")



