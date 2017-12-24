import sqlite3
import tkinter
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

BUFSIZ = 1024
# connect to the database
db = sqlite3.connect("ChatDB", check_same_thread=False, timeout=5)
# get a cursor
cursor = db.cursor()
create_query = "CREATE TABLE IF NOT EXISTS chatHistory(messages text)"
# execute the query
cursor.execute(create_query)
result = cursor.execute("SELECT messages FROM chatHistory")
insert_query = "INSERT INTO chatHistory(messages) VALUES(?)"


# look out for any incoming messages
def receive():
    while True:
        try:
            # receive the message
            message = client_socket.recv(BUFSIZ).decode("utf8")
            # add the message to the list
            message_list.insert(tkinter.END, message)  # message_list.insert(index, message)
            args = (message,)
            # execute the query
            cursor.execute(insert_query, args)
            # commit the changes
            db.commit()
        except OSError:
            break


def send(event=None):
    '''
    We’re using event as an argument because it is implicitly passed by Tkinter 
    when the send button on the GUI is pressed since an event is triggered.
    '''
    # typed_message is the input field on the GUI and we are extracting the message from it
    message = typed_message.get()
    # clear the input field
    typed_message.set("")
    client_socket.send(bytes(message, "utf8"))
    args = (message,)
    # execute the query
    cursor.execute(insert_query, args)
    # commit the changes
    db.commit()


# We define one more function, which will be called when we choose to close the GUI window.
def on_closing(event=None):
    # tell the server that you want to quit
    typed_message.set("quit")
    # make a call to the send() function
    send()
    # close the client socket
    client_socket.close()
    # destroy the window
    window.destroy()


# create a window
window = tkinter.Tk()
# set a title
window.title("Chat App")
# create a message frame to display the messages
message_frame = tkinter.Frame(window)
# we store the input field of the message frame into a variable
typed_message = tkinter.StringVar()
# we put a default message into the message frame
typed_message.set("Start chatting!")
# put a scroll bar for the message frame
scrollbar = tkinter.Scrollbar(message_frame)
# define a message_list which will list all the messages and it will be stored in the message frame
message_list = tkinter.Listbox(message_frame, height=15, width=50, yscrollcommand=scrollbar.set)
# pack the widgets at appropriate places
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
message_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
message_list.pack()
message_frame.pack()
# create input field for the user to input their message and bind it to the string variable create above
entry_field = tkinter.Entry(window, textvariable=typed_message)
# also bind the input field to the send function so that when user presses 'return', the message is sent
entry_field.bind("return", send)
# pack the widgets at appropriate places
entry_field.pack()
# create a send button if the user want to press the button to send the message
send_button = tkinter.Button(window, text="Send", command=send)
# pack the widgets at appropriate places
send_button.pack()

'''
Tkinter supports a mechanism called protocol handlers. Here, the term protocol refers to the 
interaction between the application and the window manager. The most commonly used protocol 
is called WM_DELETE_WINDOW, and is used to define what happens when the user explicitly closes 
a window using the window manager.
You can use the protocol method to install a handler for this protocol 
'''
# when the user closes the window, on_closing() method will be called
window.protocol("WM_DELETE_WINDOW", on_closing)

# ask the user for the host/server address
HOST = input("Enter host: ")
# ask the user for the host port
PORT = input("Enter port: ")
if not PORT:
    PORT = 33000  # give a default port if not provided by the user
else:
    PORT = int(PORT)
# address tuple containing connection address and port number
ADDR = (HOST, PORT)
# create a client socket
client_socket = socket(AF_INET, SOCK_STREAM)
# connect the client socket to the server
client_socket.connect(ADDR)
for row in result:
    message_list.insert(tkinter.END, row)
# create a thread to receive messages
receive_thread = Thread(target=receive)
# start the thread
receive_thread.start()
# start the GUI execution
tkinter.mainloop()
