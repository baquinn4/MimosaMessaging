
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import sys
import os


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("") # Clears input field.
    client_socket.send(bytes(msg, "utf8"))



def on_closing(event=None):
    """This function is to be called when the window is closed."""
    client_socket.close()
    master.destroy()


def relogin_verify():
    return
    

def login_verify():
    username = username_login_entry.get()
    password = password_login_entry.get()
    users = ["Maddie","Zach T","Zach R","Mason","Steve","Joey","Christina","Grace","Brad","Jordyn"]
    if username in users and password == 'mimosa1337':
        f = open(os.path.join(__location__, 'credents.txt'),'w+')
        f.write(username + "\n")
        f.write(password)
        f.close()
        login_screen.destroy()
        return 


def login():
    global __location__
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    if os.path.exists("credents.txt"):
        relogin_verify()
    else:
        f = open(os.path.join(__location__, 'credents.txt'),'w+')
        f.close()
        global login_screen
        login_screen = tkinter.Tk()
        login_screen.title("Login")
        login_screen.geometry("300x250")

        labe1= tkinter.Label(login_screen, text="Use your name, first letter capitalized").pack()
        label2= tkinter.Label(login_screen, text="").pack()
        
        global username_login_entry
        global password_login_entry

        userlabel = tkinter.Label(login_screen, text="Username * ").pack()
        username_login_entry = tkinter.Entry(login_screen)
        username_login_entry.pack()

        spacelabel = tkinter.Label(login_screen, text="").pack()

        passlabel = tkinter.Label(login_screen, text="Password * ").pack()
        password_login_entry = tkinter.Entry(login_screen,show= '*')
        password_login_entry.pack()

        spacelabel2 = tkinter.Label(login_screen, text="").pack()
        

        loginbutton = tkinter.Button(login_screen, text="Login", width=10, height=1,command=login_verify).pack()
    
 
        login_screen.mainloop()


def master():
    global username
    f = open(os.path.join(__location__, 'credents.txt'),'r')
    username = f.read().split()[0]
    f.close()
    global master
    master = tkinter.Tk()
    master.title("Mimosa Messaging")
    master.geometry("1000x600")

    userstatusframe = tkinter.LabelFrame(master,text="User's Online",height=300,width=100)
    userstatusframe.place(x=10,y=0)

    messages_frame = tkinter.LabelFrame(master,text="Chat",height=270,width=990)
    messages_frame.grid(row=2, column=4, columnspan=1, sticky="E",padx=5, pady=5, ipadx=0, ipady=0)
    messages_frame.pack(side='bottom',padx=0,pady=10)

    

    scrollbar = tkinter.Scrollbar(messages_frame,orient=tkinter.VERTICAL)
    scrollbar.pack(side=tkinter.RIGHT,fill=tkinter.Y)

    global msg_list
    msg_list = tkinter.Listbox(messages_frame, height=11, width=118,yscrollcommand=scrollbar.set)

    msg_list.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=msg_list.yview)

    msg_list.pack(side=tkinter.TOP,fill=tkinter.BOTH)

    global my_msg
    my_msg = tkinter.StringVar()
     

    sendmsg_field = tkinter.Entry(messages_frame, textvariable=my_msg,width=50)
    sendmsg_field.bind("<Return>", send)
    sendmsg_field.pack(side=tkinter.BOTTOM,fill=tkinter.X)
    
    

    master.protocol("WM_DELETE_WINDOW", on_closing)

    #----Now comes the sockets part----
    HOST = '96.126.117.230'
    PORT = 80
    global BUFSIZ
    BUFSIZ = 1024
    ADDR = (HOST, PORT)
    
    global client_socket
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(ADDR)

    receive_thread = Thread(target=receive)
    receive_thread.start()
    tkinter.mainloop()  # Starts GUI execution.

def main():
    login()
    master()

main()
