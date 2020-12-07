
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import sys
import os
from io import StringIO
import errno
import datetime

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

	def __init__(self):
		tkinter.Tk.__init__(self)
		self.title("Mimosa Messaging")
		self.geometry("550x450")
		self.configure(bg='bisque2')
		
		spacelb = tkinter.Label(self,text="",bg='bisque2').pack()
		self.labe1= tkinter.Label(self, text="Welome my dude/dudette",bg='bisque2').pack()
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

	
	def setCredents(self):

		self.cred_list.append(self.username_login_entry.get())
		self.cred_list.append(self.password_login_entry.get())
		self.destroy()

	def getCredents(self):
		return self.cred_list

class MasterInterface():

	def __init__(self,User,client_socket,BUFSIZ):

		self.commands_dict = {"quit()" : " | closes program [you can also just click x at top right], quit() may take two attempts", 
							"users()" : "| lists users currently online",
							"bug()" : "  | use this to report a bug -- usage: bug() [space] whatever you want to report",
							"priv()" : " | use this to private message -- usage: priv() [space] [user_to_priv_msg] [space] [your message]"
							}
		self.BUFSIZ = BUFSIZ
		self.client_socket = client_socket
		self.window = tkinter.Tk()
		self.window.title("Mimosa Messaging")
		self.window.geometry("1000x600")
		self.window.protocol("WM_DELETE_WINDOW", self.close_window)
		
		self.updateframe = tkinter.LabelFrame(self.window,text="Updates will be listed here maybe",height=300,width=115,font=('Consolas', 10))
		self.updateframe.place(x=12,y=5)
		
		self.s1label = tkinter.Label(self.updateframe,text="---------------------------------------------")
		self.s1label.pack(fill=tkinter.X)

		self.updateButton = tkinter.Button(self.updateframe,text="Update",width=10,height=1).pack()



		self.messages_frame = tkinter.LabelFrame(self.window,text="Chat",height=270,width=990)
		self.messages_frame.grid(row=2, column=4, columnspan=1, sticky="E",padx=5, pady=5, ipadx=0, ipady=0)
		self.messages_frame.pack(side='bottom',padx=0,pady=10)

		self.scrollbar = tkinter.Scrollbar(self.messages_frame,orient=tkinter.VERTICAL)
		self.scrollbar.pack(side=tkinter.RIGHT,fill=tkinter.Y)

		self.msg_list = tkinter.Listbox(self.messages_frame, height=11, width=118,yscrollcommand=self.scrollbar.set,fg='dark goldenrod',bg='lavender',font=('Consolas', 10))

		self.msg_list.configure(yscrollcommand=self.scrollbar.set)
		self.scrollbar.configure(command=self.msg_list.yview)

		self.msg_list.pack(side=tkinter.TOP,fill=tkinter.BOTH)
		
		self.my_msg = tkinter.StringVar()
		self.sendmsg_field = tkinter.Entry(self.messages_frame, textvariable=self.my_msg,width=50,fg='black',bg='lavender',font=('Consolas', 10))
		self.sendmsg_field.bind("<Return>", self.send)
		self.sendmsg_field.pack(side=tkinter.BOTTOM,fill=tkinter.X)


		self.User = User
		
		self.client_socket.send(bytes(self.User.getName(),"utf8"))

		self.client_socket.send(bytes(self.User.getName(),"utf8"))

		receive_thread = Thread(target=self.receive)
		receive_thread.start()


	def close_window(self):
		self.my_msg.set("quit()")
		self.send()

	
	def receive(self):
		while True:
			try:
    
				curr_time_UTC = datetime.datetime.now()
				day_name = curr_time_UTC.strftime('%a')
				am_or_pm = curr_time_UTC.strftime('%p')

				hour_min = curr_time_UTC.strftime("%I:%M")

				hour_minute_day_UTC = "| %s %s  %s |" % (hour_min,am_or_pm,day_name)

				msg = self.client_socket.recv(self.BUFSIZ).decode("utf8")

				pm_tag = msg[0:2]


				if "for a list of commands" in msg:
					dashes = ""
					for i in range(0,len(msg)):
						dashes = dashes + "-"
					self.msg_list.insert(tkinter.END," ")
					self.msg_list.insert(tkinter.END, msg)
					self.msg_list.itemconfig(tkinter.END,{'fg':'black'})
					self.msg_list.insert(tkinter.END,dashes)
					self.msg_list.itemconfig(tkinter.END,{'fg':'black'})
				elif "has left the chat." in msg:
					self.msg_list.insert(tkinter.END,msg)
					self.msg_list.itemconfig(tkinter.END, {'fg':'purple'})
					self.msg_list.see(tkinter.END)
				elif "has joined the chat!" in msg:
					self.msg_list.insert(tkinter.END,msg)
					self.msg_list.itemconfig(tkinter.END, {'fg':'purple'})
					self.msg_list.see(tkinter.END)
				elif msg == "-l":
					self.msg_list.insert(tkinter.END,"Commands:")
					self.msg_list.itemconfig(tkinter.END, {'fg':'blue'})
					for key,value in self.commands_dict.items():
						self.msg_list.insert(tkinter.END,"     --> " + key + value)
						self.msg_list.itemconfig(tkinter.END, {'fg':'blue'})
						self.msg_list.see(tkinter.END)
				elif "[" in msg and "]" in msg:
					dashes = "------------"
					for i in range(0,len(msg)):
						dashes = dashes + "-"
					self.msg_list.insert(tkinter.END,dashes)
					self.msg_list.see(tkinter.END)
					self.msg_list.itemconfig(tkinter.END,{'fg':'black'})
					self.msg_list.insert(tkinter.END, "Users online: " + msg)
					self.msg_list.see(tkinter.END)
					self.msg_list.itemconfig(tkinter.END,{'fg':'black'})
					self.msg_list.insert(tkinter.END,dashes)
					self.msg_list.see(tkinter.END)
					self.msg_list.itemconfig(tkinter.END,{'fg':'black'})
				elif msg == "Bug reported thanks nerdXyxm":
					self.msg_list.insert(tkinter.END, "Bug reported thanks nerd")
					self.msg_list.itemconfig(tkinter.END,{'fg':'green'})
					self.msg_list.see(tkinter.END)
				# elif pm_tag == "PM":
				# 	self.msglist.insert(tkinter.END,msg[pm_tag+1:])
				# 	self.msg_list.itemconfig(tkinter.END, {'fg':'red'})
				# 	self.msg_list.see(tkinter.END)
				elif "PrivMsg" in msg:
					self.msg_list.insert(tkinter.END,msg)
					self.msg_list.itemconfig(tkinter.END, {'fg':'red'})
					self.msg_list.see(tkinter.END)

				else:
					msg_pad_hmd = f'{msg: <{94}}  {hour_minute_day_UTC}'
					self.msg_list.insert(tkinter.END, msg_pad_hmd)
					self.msg_list.see(tkinter.END)
					
			except OSError: # Possibly client has left the chat.
				break

	
	def send(self,event=None):  # event is passed by binders.
	
		msg = self.my_msg.get()
		try:
			index = msg.index(">")
			msg = msg[index+2:]
		except ValueError:
			pass	
		self.my_msg.set("--> ")  # Clears input field.
		try:
			self.client_socket.send(bytes(msg, "utf8"))
		except OSError:
			sys.exit()
		if msg == "quit()":
			self.client_socket.close()
			self.window.quit()
			

ADDR = ('96.126.117.230',33000)
socket = socket(AF_INET, SOCK_STREAM)


global error_string
error_string = ""

global check_to_kill
check_to_kill = False

try:
	socket.connect(ADDR)
except OSError as e:
		x,y = e.args
		error_string = y
		
print(error_string)
if error_string != "":
	check_to_kill = True
	error_screen = tkinter.Tk()	
	error_screen.title("Mimosa Messaging")
	error_screen.geometry("550x450")
	error_screen.configure(bg='bisque2')

	spacelb1 = tkinter.Label(error_screen,text="",bg='bisque2').pack()
	spacelb2 = tkinter.Label(error_screen,text="",bg='bisque2').pack()
	spacelb3 = tkinter.Label(error_screen,text="",bg='bisque2').pack()

	if error_string == "Connection refused":
		labe1= tkinter.Label(error_screen, text="Our server is down, we will be back online ASAP",bg='bisque2').pack()
	elif error_string == "Network unreachable":
		labe1= tkinter.Label(error_screen, text="Seems like you're not connected to the internet, check that out",bg='bisque2').pack()
	else:
		labe1= tkinter.Label(error_screen, text="Unknown error woops",bg='bisque2').pack()
	
	error_exit_button = tkinter.Button(error_screen, text="exit", width=10, height=1,command=error_screen.destroy,bg='bisque2').pack(side=tkinter.BOTTOM)
	error_screen.mainloop()

if check_to_kill == True:
	sys.exit()
login = LoginInterface()
login.mainloop()
print(login.cred_list)
user = User(login.getCredents()[0],login.getCredents()[1])

master = MasterInterface(user,socket,1024)
master.window.mainloop()



