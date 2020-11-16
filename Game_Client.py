import random 
import socket
import threading
import time
import sys
import msvcrt
import datetime
game=0
number=0
info = open("info_client.txt", 'a')
info.write('%-15s' %'New game'+datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")+"\n")
try:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(("127.0.0.1",4000))
except socket.error:
           print("Failed to create socket")

print('Connect to:',"127.0.0.1,4000")
def Commands(userInput,s):
    global game
    flag=0
    if(userInput=="Game"):
        flag=1
        s.send("Game\r\n".encode())
        info.write('%-15s' % 'Game'+datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")+"\n")
        ready = s.recv(80).decode()
        if ready == "Ready\r\n":
            game=1
            mode=input("Choose entering numbers by hands(1) or random(2): ")
            Game(userInput,s,mode)
            
    elif(userInput=="Open number"):
        flag=1
        global number
        if(game==1):
            s.send("Open number\r\n".encode())
            info.write('%-15s' % 'Open number'+datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")+"\n")
            number = s.recv(80).decode()
            print("The number was: ",number)
            game=0
        else:
            print('There no current game to open a number!')
            print("Previous was: ",number)

    elif(userInput=="Who"):
        flag=1
        print("Olena Namaka #18 lab work 2\n You can use commands: Game, Who, Open number, End \n")
    elif(userInput=="End"):
        flag=1
        s.send("End\r\n".encode())
        info.write('%-15s' % 'End'+datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")+"\n")
        print("Good bye,hope to see you soon")
        s.close()
        exit(0)
        return
    elif(flag==0):
        print("Wrong command!")
    message = (input("Write command: "))
    Commands(message,s)

def Game(message,s,mode):
    global game
    answer=0
    while True:
        if(mode=='1'):
            answer=""
            while(not(answer.isdigit() and (int(answer)>=1000 and int(answer)<10000))):
                answer = str(((input("Guess the 4 digit number: "))))
                if(answer==""):
                    break
        elif(mode=='2'):
            time.sleep(2)
            answer=str(random.randrange(1000, 10000))
            print(answer,end='\n')
        if(msvcrt.kbhit()or (answer=='')):
            print('End current guessing game')
            if(mode=='2'):
                test=(input())
            break
        try:
            s.send(answer.encode())
            info.write('%-15s' %answer+datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")+"\n")
            message= int(s.recv(80).decode())
        except :
            print("Host closed connection forcibly")
            s.close()
            exit(0)
        result=Result(message)
        if(result==True):
            game=0
            break
    message = (input("Write command: "))
    Commands(message,s)

def Result(message):
    count_pos=int(message/10)
    count_amount=message%10
    if(count_pos==4 and count_amount==4):
        print("Good job!!! You won :)\n")
        return True
    elif((count_pos <= 4) and (count_pos != 0)) or ((count_amount <= 4) and (count_amount != 0)):
            print("Not quite the number. But you did get ", count_pos, " digit(s) put in correct position!") 
            print("Also total ",count_amount," numbers  in your input were correct,but not all in correct position.\n")
            return False
    elif (count_pos==0) and (count_amount==0):
            print("None of the numbers in your input match.\n")
            return False


s.send("Hello\r\n".encode())
info.write('%-15s' % 'Hello'+datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")+"\n")
greet = s.recv(80).decode()
if greet == "Greetings\r\n":
    message = (input("Write command: "))
    Commands(message,s)
info.close()



