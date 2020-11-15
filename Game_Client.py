import random 
import socket
import threading
import time
flag=1
command=0
game=0
try:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(("127.0.0.1",4000))
except socket.error:
           print("Failed to create socket")

print('Connect to:',"127.0.0.1,4000")
def Commands(userInput,s):
    global command
    global game
    if(userInput=="Game"):
        s.send("Game\r\n".encode())
        ready = s.recv(80).decode()
        if ready == "Ready\r\n":
            game=1
            command=1
            mode=input("Choose mode by hands(1) or random(2):  ")
            threading.Thread(target =Game, args = (userInput,s,mode,game)).start()
            if(mode=='2'):
                threading.Thread(target=get_input).start()
            
    elif(userInput=="Open number"):
        if(game==1):
            s.send("Open number\r\n".encode())
            number = s.recv(80).decode()
            print("The number was: ",number)
        else:
            print('There no current game to open a number!')

    elif(userInput=="Who"):
        print("Olena Namaka #18 lab work 2")
    elif(userInput=="End"):
        s.send("End\r\n".encode())
        print("Good bye,hope to see you soon")
        s.close()
        return
    if(command==0):
        message = (input("Write command: "))
        Commands(message,s)

def Game(message,s,mode,game):
    global flag
    global command
    answer=0
    flag=1
    while True:
        if(mode=='1'):
            answer = str(input("Guess the 4 digit number:"))
        elif(mode=='2'):
            answer=str(random.randrange(1000, 10000))
        if((flag==False) or (answer=='')):
            print('End cuurent guessing game')
            break
        s.send(answer.encode())
        message= int(s.recv(80).decode())
        result=Result(message)
        time.sleep(2)
        if(result==True):
            game=0
            break
    command=0
    message = (input("Write command: "))
    Commands(message,s)

def Result(message):
    count_pos=int(message/10)
    count_amount=message%10
    if ((count_pos < 4) and (count_pos != 0)) or ((count_amount < 4) and (count_amount != 0)):
            print("Not quite the number. But you did get ", count_pos, " digit(s) put in correct position!") 
            print("Also total ",count_amount," numbers  in your input were correct,but not all in correct position.")
            return False
    elif (count_pos==0) and (count_amount==0):
            print("None of the numbers in your input match.")
            return False
    else:
            print("Good job!!! You win :)")
            return True
def get_input():
    global flag
    keystrk=input()
    flag=False

s.send("Hello\r\n".encode())
greet = s.recv(80).decode()
if greet == "Greetings\r\n":
    message = (input("Write command: "))
    Commands(message,s)



