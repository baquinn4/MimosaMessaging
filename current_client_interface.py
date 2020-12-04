
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import sys
import os
from io import StringIO
import errno


# set(
# 	name = 'current_client_interace.py',
# 	version = '0.0.1',
# 	entry_points={})

class User:
	def __init__(self,username,password):
		self.username = username
		self.password = password
		
	def getName(self):
		return self.username

	def getPass(self):
		return self.password

	def setName(self,username):
		self.username = username

	def setPass(password):
		self.password = password



class LoginInterface(tkinter.Tk):

	# def __init__(self,HOST='96.126.117.230',PORT=80,BUFSIZ=1024):
	# 	self.HOST = HOST
	# 	self.PORT = PORT
	# 	self.BUFSIZ = BUFSIZ

	def __init__(self):
		tkinter.Tk.__init__(self)
		self.title("Login")
		self.geometry("550x450")
		self.configure(bg='bisque2')
		

		spacelb = tkinter.Label(self,text="",bg='bisque2').pack()
		labe1= tkinter.Label(self, text="Welome my dude/dudette",bg='bisque2').pack()
		label2= tkinter.Label(self, text="",bg='bisque2').pack()

		userlabel = tkinter.Label(self, text="Username",bg='bisque2').pack()

		self.username = tkinter.StringVar()
		self.username_login_entry = tkinter.Entry(self,bg='linen')
		self.username_login_entry.pack()

		spacelabel = tkinter.Label(self, text="",bg='bisque2').pack()

		passlabel = tkinter.Label(self, text="Password",bg='bisque2').pack()

		self.password_login_entry = tkinter.Entry(self,show= '*',bg='linen')
		self.password_login_entry.pack()

		spacelabel2 = tkinter.Label(self, text="",bg='bisque2').pack()
		self.cred_list = []

		loginbutton = tkinter.Button(self, text="Login", width=10, height=1,command=self.setCredents,bg='bisque2').pack()
		
		

	# def main(self):
	# 	self.BuildLoginInterface()
	# 	print(self.User.getName())
	
	def setCredents(self):

		self.cred_list.append(self.username_login_entry.get())
		self.cred_list.append(self.password_login_entry.get())
		self.destroy()

	def getCredents(self):
		return self.cred_list



class MasterInterface():

	def __init__(self,User,client_socket,BUFSIZ):
		self.BUFSIZ = BUFSIZ
		self.client_socket = client_socket
		self.window = tkinter.Tk()
		self.window.title("Mimosa Messaging")
		self.window.geometry("1000x600")
		self.window.protocol("WM_DELETE_WINDOW", self.close_window)

		self.userstatusframe = tkinter.LabelFrame(self.window,text="User's Online",height=300,width=100)
		self.userstatusframe.place(x=10,y=0)




		self.messages_frame = tkinter.LabelFrame(self.window,text="Chat",height=270,width=990)
		self.messages_frame.grid(row=2, column=4, columnspan=1, sticky="E",padx=5, pady=5, ipadx=0, ipady=0)
		self.messages_frame.pack(side='bottom',padx=0,pady=10)

		self.scrollbar = tkinter.Scrollbar(self.messages_frame,orient=tkinter.VERTICAL)
		self.scrollbar.pack(side=tkinter.RIGHT,fill=tkinter.Y)

		self.msg_list = tkinter.Listbox(self.messages_frame, height=11, width=118,yscrollcommand=self.scrollbar.set,fg='dark goldenrod',bg='lavender')

		self.msg_list.configure(yscrollcommand=self.scrollbar.set)
		self.scrollbar.configure(command=self.msg_list.yview)

		self.msg_list.pack(side=tkinter.TOP,fill=tkinter.BOTH)
		
		self.my_msg = tkinter.StringVar()
		self.sendmsg_field = tkinter.Entry(self.messages_frame, textvariable=self.my_msg,width=50,fg='black',bg='lavender')
		self.sendmsg_field.bind("<Return>", self.send)
		self.sendmsg_field.pack(side=tkinter.BOTTOM,fill=tkinter.X)


		self.User = User
		
		self.client_socket.send(bytes(self.User.getName(),"utf8"))

		receive_thread = Thread(target=self.recieve)
		receive_thread.start()

		


	def close_window(self):
		self.my_msg.set("-q")
		self.send()

		

	def recieve(self):
		while True:
			try:
				msg = self.client_socket.recv(self.BUFSIZ).decode("utf8")
				self.msg_list.insert(tkinter.END, msg)
			except OSError: # Possibly client has left the chat.
				break

	
	def send(self,event=None):  # event is passed by binders.

		try:
			msg = self.my_msg.get()
			self.my_msg.set("") # Clears input field.
			self.client_socket.send(bytes(msg, "utf8"))
			if msg == "-q":
				self.client_socket.close()
				self.window.destroy()
		except OSError:
			pass
		

	# def close_window(self):
	# 	global running
	# 	running = False
	# 	print("ok")
	# 	process = subprocess.Popen(['send.exe'],stdout=subprocess.PIPE,shell=True)



	# def on_closing(self,event=None):
	# 	self.client_socket.close()
	# 	self.window.destroy()

	

	

		#self.protocol("WM_DELETE_WINDOW", on_closing)
		


	# def BuildLoginInterface(self):

	# 	login_screen = tkinter.Tk()
	# 	login_screen.title("Login")
	# 	login_screen.geometry("300x250")

	# 	labe1= tkinter.Label(login_screen, text="Welome").pack()
	# 	label2= tkinter.Label(login_screen, text="").pack()

	# 	userlabel = tkinter.Label(login_screen, text="Username * ").pack()

	# 	username_login_entry = tkinter.Entry(login_screen)
	# 	username_login_entry.pack()

	# 	spacelabel = tkinter.Label(login_screen, text="").pack()

	# 	passlabel = tkinter.Label(login_screen, text="Password * ").pack()

	# 	password_login_entry = tkinter.Entry(login_screen,show= '*')
	# 	password_login_entry.pack()

	# 	spacelabel2 = tkinter.Label(login_screen, text="").pack()

	# 	print(username_login_entry.get())
	# 	self.User = User(username_login_entry.get(),password_login_entry.get())
	# 	print(self.User)
		

	# 	loginbutton = tkinter.Button(login_screen, text="Login", width=10, height=1,command=self.printt).pack()
	# 	login_screen.mainloop()
		
	# #def BuildMainInterface(self):

	# 	self.master = tkinter.Tk()
	# 	self.master.title("Mimosa Messaging")
	# 	self.master.geometry("1000x600")

	# 	userstatusframe = tkinter.LabelFrame(self.master,text="User's Online",height=300,width=100)
	# 	userstatusframe.place(x=10,y=0)

	# 	messages_frame = tkinter.LabelFrame(self.master,text="Chat",height=270,width=990)
	# 	messages_frame.grid(row=2, column=4, columnspan=1, sticky="E",padx=5, pady=5, ipadx=0, ipady=0)
	# 	messages_frame.pack(side='bottom',padx=0,pady=10)

	# 	scrollbar = tkinter.Scrollbar(messages_frame,orient=tkinter.VERTICAL)
	# 	scrollbar.pack(side=tkinter.RIGHT,fill=tkinter.Y)

	# 	self.msg_list = tkinter.Listbox(messages_frame, height=11, width=118,yscrollcommand=scrollbar.set)

	# 	self.msg_list.configure(yscrollcommand=scrollbar.set)
	# 	scrollbar.configure(command=self.msg_list.yview)

	# 	self.msg_list.pack(side=tkinter.TOP,fill=tkinter.BOTH)
		
	# 	self.my_msg = tkinter.StringVar()
	# 	sendmsg_field = tkinter.Entry(messages_frame, textvariable=my_msg,width=50)
	# 	sendmsg_field.bind("<Return>", send)
	# 	sendmsg_field.pack(side=tkinter.BOTTOM,fill=tkinter.X)

	# 	self.master.protocol("WM_DELETE_WINDOW", on_closing)
	# 	tkinter.mainloop()

	

	


ADDR = ('96.126.117.230',80)
socket = socket(AF_INET, SOCK_STREAM)

try:
	socket.connect(ADDR)
except ConnectionRefusedError:
	print("ERROR 111")
		
login = LoginInterface()
login.mainloop()
print(login.cred_list)
user = User(login.getCredents()[0],login.getCredents()[1])

master = MasterInterface(user,socket,1024)
master.window.mainloop()



