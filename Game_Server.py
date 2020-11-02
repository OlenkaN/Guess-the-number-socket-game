import random 
import socket
import threading


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
def Commands(message,clientsocket,clientaddress):
	if(message=="Game\r\n"):
		Game(message,clientsocket,clientaddress)
	elif(message=="End\r\n"):
		print("End work with ",clientaddress)
		clientsocket.close()
def Game(message,clientsocket,clientaddress):
	#generate number to guess
	num1 = random.randrange(1000, 10000)
	while message == "Game\r\n":
		clientsocket.send("Ready\r\n".encode())
		try:
		   n = clientsocket.recv(1024).decode()	
		except ConnectionResetError:
			print("Client closed connection forcibly")
			clientsocket.close()
			break
		count=Calculate(num1,n)
		if(count==44):
		   clientsocket.send(str(count).encode())
		   print("User has won.")
		   message = clientsocket.recv(80).decode()
		   Commands(message,clientsocket,clientaddress)
		   break
		else:
			clientsocket.send(str(count).encode())
		message = clientsocket.recv(80).decode()
	if(message=="Open number\r\n"):
		clientsocket.send(str(num1).encode())
		message = clientsocket.recv(80).decode()
	Commands(message,clientsocket,clientaddress)
	


def handleclient(clientsocket,clientaddress):
	# Receive the client's greeting
	clientgreeting = clientsocket.recv(1024).decode()
	# Send the welcome message to the client
	welcomemessage = "Greetings\r\n"
	clientsocket.send(welcomemessage.encode())
	message = clientsocket.recv(1024).decode()
	Commands(message,clientsocket,clientaddress)








print('waits for player to connect')
while 1:
	(clientsocket, clientaddress) = s.accept()
	print("Connection received from: ", clientaddress)
	threading.Thread(target = handleclient, args =  (clientsocket,clientaddress)).start()
	print("Connection passed to new thread. Returning to listening.")

