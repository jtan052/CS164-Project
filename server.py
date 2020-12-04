import socket
import sys
from thread import *
import time

'''
Function Definition
'''
def tupleToString(t):
	s=""
	for item in t:
		s = s + str(item) + "<>"
	return s[:-2]

def stringToTuple(s):
	t = s.split("<>")
	return t

'''
Create Socket
'''
HOST = ''	# Symbolic name meaning all available interfaces
PORT = 9486	# Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print 'Socket created'

'''
Bind socket to local host and port
'''
try:
	s.bind((HOST, PORT))
except socket.error , msg:
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()
print 'Socket bind complete'

'''
Start listening on socket
'''
s.listen(10)
print 'Socket now listening'

'''
Define variables:
username && passwd
message queue for each user
'''


clients = []
# TODO: Part-1 : create a var to store username && password. NOTE: A set of username/password pairs are hardcoded here. 
userpass = [['Jacob','Tan'],['Haley','Lorenz'],['Grace','Tran']]
online = [0,0,0]
messages = [[],[],[]]
groups = [[],[],[]]
groupmsgs = [[],[],[]]
unread = [0,0,0]
count = 0

'''
Function for handling connections. This will be used to create threads
'''
def clientThread(conn):
	global clients
	global count
	# Tips: Sending message to connected ient
	#conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
	rcv_msg = conn.recv(1024)
	rcv_msg = stringToTuple(rcv_msg)
	if rcv_msg in userpass:
		user = userpass.index(rcv_msg)
		online[user] = 1
		try :
			conn.sendall('valid')
		except socket.error:
			print 'Send failed'
			sys.exit()
		#conn.send('Welcome to the server. Type something and hit enter\n')	
		# Tips: Infinite loop so that function do not terminate and thread do not end.
		while True:
			try :
				option = conn.recv(1024)
			except:
				break
			if option == str(1):
				print 'user logout'
				# TODO: Part-1: Add the logout processing here
				online[user] = 0
				conn.close()	
			elif option == str(2):
				print 'Sending Message'
				message = conn.recv(1024)
				if message == str(1):
					print 'Private Message Case'
					pmsg = conn.recv(1024)
					rcv_id = conn.recv(1024)
					if online[int(rcv_id)] == 1: #then the user is online
						for x in clients:
							x.sendall(userpass[int(rcv_id)][0] + "<>"  +  pmsg)
					else:
						messages[int(rcv_id)].append(pmsg)
						print messages[int(rcv_id)][0]
					print 'end of private message case'
				if message == str(2):
					print 'Broadcast Message Case'
					bmsg = conn.recv(1024)
					for x in clients:
						x.sendall("broadcast" + "<>" + bmsg)
					print 'end of broadcast message case'
				if message == str(3):
					print 'Send Group Message Case'
					gmsg = conn.recv(1024)
					g_id = conn.recv(1024)
					groupmsgs[int(g_id)].append(gmsg)
					print groupmsgs[int(g_id)][0]
					print 'end of groupmsg case'


			elif option == str(3):
				print 'Join/Quit group'
				message = conn.recv(1024)
				if message == str(1):
					group = conn.recv(1024)
					groups[int(group)].append(user)
					for x in groups[int(group)]:
						print type(x)
						print groups[int(group)][x]
				if message == str(2):
					group = conn.recv(1024)
					groups[int(group)].remove(user)
					for x in groups[int(group)]:
						print groups[int(group)][x]
			elif option == str(4):
				print 'View Unread Messages'
				option = conn.recv(1024)
				if option == str(1):
					for x in messages[user]:
						print messages[user][x] + '\n'
				if option == str(2):
					g_id = conn.recv(1024)
					#print 'g_id:' +  g_id
					msgnum = 1
					sendbuffer = 'gmsg'
					for msgs in groupmsgs[int(g_id)]:
						sendbuffer += "<>" + str(msgnum) + ": " + msgs
						msgnum = msgnum + 1
					conn.sendall(sendbuffer)
			elif option == str(5):
				print 'Change password'
				#conn.sendall('Server Requests Old Password\n')
				option = conn.recv(1024)
				print 'Old Password recieved: ' +  option
				print 'Old Password was: ' + userpass[user][1]
				if userpass[user][1] == option:	
					option = conn.recv(1024) #gets new password
					name = userpass[user][0]
					userpass[0] = [ name, option ]
					print 'Updated Login: ' + str(userpass[0])
				else:
					#conn.sendall('invalid')
					print 'Old Password Invalid, login info not updated'
			
			else:
				try :
					conn.sendall('Option not valid')
				except socket.error:
					print 'option not valid Send failed'
					conn.close()
					clients.remove(conn)
	else:
		try :
			conn.sendall('nalid')
		except socket.error:
			print 'nalid Send failed'
	print 'Logged out'
	#print rcv_msg
	conn.close()
	if conn in clients:
		clients.remove(conn)

def receiveClients(s):
	global clients
	while 1:
		# Tips: Wait to accept a new connection (client) - blocking call
		conn, addr = s.accept()
		print 'Connected with ' + addr[0] + ':' + str(addr[1])
		clients.append(conn)
		# Tips: start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
		start_new_thread(clientThread ,(conn,))

start_new_thread(receiveClients ,(s,))

'''
main thread of the server
print out the stats
'''
while 1:
	message = raw_input()
	if message == 'messagecount':
		print 'Since the server was opened ' + str(count) + ' messages have been sent'
	elif message == 'usercount':
		print 'There are ' + str(len(clients)) + ' current users connected'
	elif message == 'storedcount':
		print 'There are ' + str(sum(len(m) for m in messages)) + ' unread messages by users'
	elif message == 'newuser':
		user = raw_input('User:\n')
		password = raw_input('Password:')
		userpass.append([user, password])
		messages.append([])
		subscriptions.append([])
		print 'User created'
s.close()
