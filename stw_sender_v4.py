"""
This is the sender side of a stop and wait protocol. 

It does the following:

1) Asks for user input for bitstring, propogation time and probability of
package being 'dropped' between the sender and receiver. 

2) It then proceeds to send or not send (to simulate dropping in an 
unreliable channel) the bits of the input bitstring.  
"""

#make necessary imports
import socket
from threading import *
import time
import random



#------------------------------------------------------------------------
#create socket object and bind it.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "localhost"
port = 8000
s.bind((host, port))

#------------------------------------------------------------------------
#defines the class for client. 
class client(Thread):
    #initialize everything
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()


    def run(self):

        while True:

            #take input from user 
            bitstring  = str(raw_input("enter bit string"))
            propogationtime = float(raw_input("enter propogation time"))
            p_nosend = float(input("enter probability of message getting lost:"))
            
            #create a list of 1000 elements. (redundant, can be changed)
            l = []
            for i in range(0,1000):
                l = l +[i]

            #go through all the bits of the bitstring. 
            i = 0
            while i < len(bitstring):
                #for each bit, create a dictionary with the current 
                #window index (i%2 => 0,1,0,1...) and the bit itself
                datadict = {}
                datadict = {i%2 : bitstring[i], }
                
                #convert the dictionary to a string 
                sendstring = str(datadict)
                
                #find a random number between 0,1000 (both included)
                number= random.randint(0,1000)
                
                #store current time 
                time1 = time.time()
                
                #if statement is true with a probability of (1-p_nosend)
                if l[number] < (p_nosend*1000):
                    #if true, send the bitstring.
                    clientsocket.send(sendstring)
                    #sleep to simulate the propogation time of the channel.
                    time.sleep((propogationtime)/1.1)
                    #after sleeping, record the current time. 
                    time2 = time.time()
                    #this flag indicates whether an acknowledgement has been received. 
                    ackflag= False
                
                #else statement is true with a probability of (p_nosend)
                #this simulates a packet being sent but getting lost
                #along the way (like our lives). 
                else: 
                    #imaginary send line here.
                    #wait for propogation time again. 
                    time.sleep(propogationtime/1.1)
                    #record current time 
                    time2 = time.time()
                    #for info of user:
                    print ("package dropped 1")
                    #set ack flag to False, again.  
                    ackflag= False               

                while True:
                    #if the time elapsed is less that prop time, 
                    if time2-time1<= propogationtime:
                        #store current time     
                        time2= time.time()

                        #set timeout to listen for an acknowledgement. 
                        clientsocket.settimeout(propogationtime/1.1)

                        #raises exception when the timeout occurs. 
                        try:
                            #attempt to listen for ack. 
                            recieved = clientsocket.recv(1024)
                            print(recieved)
                            
                            if recieved:
                                print "ack received"
                                i = i+1
                                ackflag = True
                                break 

                        #this occurs when listening has timed out. 
                        except:
                            #recheck if it has timed out (quite redundant):
                            if time2 - time1 >propogationtime and ackflag == False:
                                print ("timeout")

                                #at this stage, we again simulate a package drop 
                                #with prob p_nosend
                                number= random.randint(0,1000)

                                #package sent
                                if l[number] < (p_nosend*1000):
                                    clientsocket.send(sendstring)
                                    time1 = time.time()
                                    time2 = time.time()
                                    print "package sent"

                                #package dropped:    
                                else: 
                                    
                                    time1 = time.time()
                                    time2 = time.time()
                                    #time.sleep(propogationtime/1.1)
                                    
                                    print("package dropped 2")

                        
                    
                    
    
            

s.listen(5)
print ('Sender ready and is listening')
while (True):

    #to accept all incoming connections
    clientsocket, address = s.accept()
    print("Receiver "+str(address)+" connected")
    #create a different thread for every 
    #incoming connection 
    client(clientsocket, address)
