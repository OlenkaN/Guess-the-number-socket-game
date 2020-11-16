import random 
import socket
import threading
import datetime
import msvcrt

info = open("info_server2.txt", 'a')
info.write('%-15s' %'New game'+datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")+"\n")
info.close()
TCP_IP = '127.0.0.1'
TCP_PORT = 4000
#Checks if client socket is created properly   
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((TCP_IP,TCP_PORT))
	s.listen(5)
except socket.error:
           print("Failed to create socket")
def Calculate(num,n):
	num=str(num)
	n=str(n)
	if(n==num):
		return 44
    #find amount of digits in correct position count_pos
    # and amount of digits that num and n have in common count_amount
	count_pos=0
	count_amount=0
	temp=num
	for i in range(0,4):
		if n[i] in temp:
			temp = temp.replace(n[i],'',1)
			count_amount+=1
		if(n[i]==num[i]):
			count_pos+=1
		else:
			continue
	return count_pos*10+count_amount
def Commands(message,clientsocket,clientaddress,info1):
	if(message=="Game\r\n"):
		clientsocket.send("Ready\r\n".encode())
		info1.write('%-15s' %'Ready'+datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")+"\t"+str(clientaddress)+"\n")
		Game(message,clientsocket,clientaddress,info1)
	elif(message=="End\r\n"):
		print("End work with ",clientaddress)
		clientsocket.close()
def num():
	mode=input("Choose entering numbers  by hands(1) or random_normal(2) or:random_Gauss(3) ")
	if(mode=='1'):
		num = str(input("Enter the 4 digit number: "))
	elif(mode=='2'):
		num=random.randrange(1000, 10000)
	else:
		mu=float(input("Choose mu from 1000 to 9999: "))
		minimum = min(mu-1000,9999-mu)
		print("Choose sigma less than",minimum)
		sigma=float(input())
		num=0
		while(not(num>=1000 and num<10000)):
			num=int(random.gauss(mu,sigma))
	return str(num)

def Game(message,clientsocket,clientaddress,info1):
	#generate number to guess
	num1 = num()
	while True:
		try:
			n = clientsocket.recv(1024).decode()	
			if(n.isdigit()):
				count=Calculate(num1,n)
				if(count==44):
				   clientsocket.send(str(count).encode())
				   info1.write('%-15s' %str(count)+datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")+"\t"+str(clientaddress)+"\n")
				   print("User has won.")
				   message = clientsocket.recv(80).decode()
				   Commands(message,clientsocket,clientaddress,info1)
				   break
				else:
				   clientsocket.send(str(count).encode())
				   info1.write('%-15s' % str(count)+datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")+"\t"+str(clientaddress)+"\n")
			else:
				message=n
				if(message=="Open number\r\n"):
					clientsocket.send(str(num1).encode())
					info1.write('%-15s' %str(num1)+datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")+"\t"+str(clientaddress)+"\n")
					message = clientsocket.recv(80).decode()
				Commands(message,clientsocket,clientaddress,info1)
				break
		except ConnectionResetError:
			print("Client closed connection forcibly")
			clientsocket.close()
			break
	


def handleclient(clientsocket,clientaddress):
	info1 = open("info_server2.txt", 'a')
	# Receive the client's greeting
	clientgreeting = clientsocket.recv(1024).decode()
	# Send the welcome message to the client
	welcomemessage = "Greetings\r\n"
	clientsocket.send(welcomemessage.encode())
	info1.write('%-15s' %'Greetings'+datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")+"\t"+str(clientaddress)+"\n")
	message = clientsocket.recv(1024).decode()
	Commands(message,clientsocket,clientaddress,info1)
	info1.close()








print('waits for player to connect')
while 1:
	(clientsocket, clientaddress) = s.accept()
	print("Connection received from: ", clientaddress)
	threading.Thread(target = handleclient, args =  (clientsocket,clientaddress)).start()
	print("Connection passed to new thread. Returning to listening.")

