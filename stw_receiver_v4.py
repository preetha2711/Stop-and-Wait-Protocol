"""
This is the receiver side of a stop and wait protocol.

It does the following : 

1) Asks for user input for probability of an acknowledgement not being sent

2) It then proceeds to send or not send (to simulate dropping in an 
unreliable channel) an acknowledgement. 

"""

#make necessary imports
import socket
import random
from ast import literal_eval


#------------------------------------------------------------------------
#create socket object and bind it.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host ="localhost"
port =8000
s.connect((host,port))

#------------------------------------------------------------------------

#take input from user 
p_noack = float(input("enter probability of acknowledgement not being sent"))
count = 0 


def try_ack(previous, current):
    if abs(previous-current) == 1:
        return True
    else:
        return False 

l = []
for i in range(0,1000):
    l = l +[i]
output = ""
   
while 2: 
    data=s.recv(8).decode()
    print("Received --> "+data)
    datadict = literal_eval(data)
    index = list((datadict).keys())[0]
    number= random.randint(0,1000)
    if count == 0:
        count = count +1
        current = index
        previous = 0
        if current == 0:
            previous = 1
    
    #simulating the acknowldgement message being lost on the way 
    else: 
        count = count +1
        previous = current
        current = index
        print ("p /c :", previous, current)
    if try_ack(previous, current):
        output  = output + list(datadict.values())[0]
        #print ("hello", l[number],p_noack*1000 )
        if l[number]<(p_noack*1000):
            print "Ack not sent"
            pass
        else:    
            str="Acknowledgement: Message Received"
            #print ("!!!!!!!!!")
            
            #print datadict.values()
            s.send(str.encode())
    else: 
        str="Acknowledgement: Message Received"
        s.send(str.encode())
        print ("indices did not match. Sending ack for previous element")
    print "the received bitstring is",output
  
s.close ()
