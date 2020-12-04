import socket
import sys
from thread import *
import getpass
import os

'''
Function Definition
'''
def receiveThread(s):
	while True:
		try:
			reply = s.recv(4096)  # receive msg from server
			reply = stringToTuple(reply)
			if reply[0] == 'broadcast':
				print reply[1]
			elif reply[0] == username:
				print reply[1]
			elif reply[0] == 'gmsg':
				for msg in reply[1:]:
					print msg
			# You can add operations below once you receive msg
			# from the server

		except:
			print "Connection closed"
			break
	

def tupleToString(t):
	s = ""
	for item in t:
		s = s + str(item) + "<>"
	return s[:-2]

def stringToTuple(s):
	t = s.split("<>")
	return t

'''
Create Socket
'''
try:
	# create an AF_INET, STREAM socket (TCP)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
	print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
	sys.exit();
print 'Socket Created'

'''
Resolve Hostname
'''
host = 'localhost'
port = 9486
try:
	remote_ip = socket.gethostbyname(host)
except socket.gaierror:
	print 'Hostname could not be resolved. Exiting'
	sys.exit()
print 'Ip address of ' + host + ' is ' + remote_ip
'''
Connect to remote server
'''
s.connect((remote_ip , port))
print 'Socket Connected to ' + host + ' on ip ' + remote_ip

'''
TODO: Part-1.1, 1.2: 
Enter Username and Passwd
'''
# Whenever a user connects to the server, they should be asked for their username and password.
# Username should be entered as clear text but passwords should not (should be either obscured or hidden). 
# get username from input. HINT: raw_input(); get passwd from input. HINT: getpass()
username = raw_input("Username: ")


password = getpass.getpass()
# Send username && passwd to server

s.send(username + '<>' + password, port)

'''
TODO: Part-1.3: User should log in successfully if username and password are entered correctly. A set of username/password pairs are hardcoded on the server side. 
'''

reply = s.recv(5)
#print reply
if reply == 'valid': # TODO: use the correct string to replace xxx here!

	# Start the receiving thread
	start_new_thread(receiveThread ,(s,))

	message = ""
	
	while True :

		# TODO: Part-1.4: User should be provided with a menu. Complete the missing options in the menu!
		message = raw_input("Choose an option (type the number): \n 1. Logout \n 2. Post a message \n 3. Join or Quit a group \n 4. Read unread messages \n 5. Change Password \n")
		
		try :
			# TODO: Send the selected option to the server
			# HINT: use sendto()/sendall()
			#response = s.recv(1024)
			if message == str(1):
				print 'Logout'
				s.sendall('1')
				s.close()
				sys.exit()
				# TODO: add logout operation
			elif message == str(2):
				print 'message'
				s.sendall('2')
				while True:
					message = raw_input("Choose an option (type the number): \n 1. Private messages \n 2. Broadcast messages \n 3. Group messages \n")
					try :
						'''
						Part-2: Send option to server
						'''
						if message == str(1):
							pmsg = raw_input("Enter your private message\n")
							try :
								s.sendall('1')
								s.sendall(pmsg)
							except socket.error:
								print 'Private Message Send failed'
								sys.exit()
							rcv_id = raw_input("Enter the recevier ID:\n")
							try :
								s.sendall(rcv_id)
								break
							except socket.error:
								print 'rcv_id Send failed'
								sys.exit()
						if message == str(2):
							bmsg = raw_input("Enter your broadcast message\n")
							try :
								s.sendall('2')
								s.sendall(bmsg)
								'''
								Part-2: Send broadcast message
								'''
								break
							except socket.error:
								print 'Broadcast Message Send failed'
								sys.exit()
						if message == str(3):
							gmsg = raw_input("Enter your group message\n")
							try :
								s.sendall('3')
								s.sendall(gmsg)
							except socket.error:
								print 'Group Message Send failed'
								sys.exit()
							g_id = raw_input("Enter the Group ID:\n")
							try :
								s.sendall(g_id)
								break
							except socket.error:
								print 'g_id Send failed'
								sys.exit()
					except socket.error:
						print 'Message Send failed'
						sys.exit() 
			elif message == str(3):
				s.sendall('3')
				option = raw_input("Do you want to: 1. Join Group 2. Quit Group: \n")
				if option == str(1):
					s.sendall('1')
					group = raw_input("Enter the Group you want to join: ")
					try :
						s.sendall(group)
					except socket.error:
						print 'group info sent failed'
						sys.exit()
				elif option == str(2):
					s.sendall('2')
					group = raw_input("Enter the Group you want to quit: ")
					try :
						s.sendall(group)
					except socket.error:
						print 'group info sent failed'
						sys.exit()
				else:
					print 'Option not valid'
			
			elif message == str(4):
				s.sendall('4')
				while not os.getpgrp() == os.tcgetpgrp(sys.stdout.fileno()):
					pass
				option = raw_input("Do you want to: 1. View all offline messages; 2. View only from a particular Group\n")
				if option == str(1):					
					try :
						s.sendall('1')
					except socket.error:
						print 'msg Send failed'
						sys.exit()
				elif option == str(2):
					s.sendall('2')
					group = raw_input("Enter the group you want to view the messages from: ")
					try :
						s.sendall(group)		
					except socket.error:
						print 'group Send failed'
						sys.exit()
				else:
					print 'Option not valid'
			# Add other operations, e.g. change password
			elif message == str(5):
				print 'Change password'
				s.sendall('5')
				#send over the old password for verification
				password = getpass.getpass(prompt='Old Password:')
				s.send(password,port)
				password = getpass.getpass(prompt= 'New Password:')
				s.sendall(password)

		except socket.error:
			print 'Send failed'
			sys.exit()
else:
	print 'Invalid username or passwword'


