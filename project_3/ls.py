import threading
import random
import socket as mysoc
import sys 
import select

import argparse
from sys import argv
import socket


# server task
def server():
    #argsv::    
    input_sys = sys.argv
    lsListenPort = int(input_sys[1])
    ts1_hostname = (input_sys[2])
    ts1_listenPort = int(input_sys[3])
    ts2_hostname = (input_sys[4])
    ts2_listenPort = int(input_sys[5])


    try:
        clientSocket=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: Server socket created for client")
    except mysoc.error as err:
        print('{} \n'.format("client socket open error ",err))
    #connection with client:
    server_binding=('',lsListenPort)

    clientSocket.bind(server_binding)
    clientSocket.listen(10)
    
    host=mysoc.gethostname()
    print("[S]: Server host name is: ",host)
    localhost_ip=(mysoc.gethostbyname(host))
    print("[S]: Server IP address is  ",localhost_ip)
 
    csockid,addr=clientSocket.accept()
    print ("[S]: Got a connection request from a client at", addr)


    try:
        ts1_Socket=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: Server socket created for ts1")
    except mysoc.error as err:
        print('{} \n'.format("ts1 socket open error ",err))

    #connections with ts1:
    
    host_ts1=mysoc.gethostbyname(ts1_hostname)
    server_binding_ts1=(host_ts1,ts1_listenPort)
    ts1_Socket.connect(server_binding_ts1)   
    ts1_Socket.settimeout(5)

    try:
        ts2_Socket=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[S]: Server socket created for ts2")
    except mysoc.error as err:
        print('{} \n'.format("ts2 socket open error ",err))    

    host_ts2=mysoc.gethostbyname(ts2_hostname)
    server_binding_ts2=(host_ts2,ts2_listenPort)
    ts2_Socket.connect(server_binding_ts2)
    ts2_Socket.settimeout(5)

    ts = 1 # set initial ts server to send to to 1 before the loop
    dict_ts1 = {} # set dicts to be blank initally before the loop
    dict_ts2 = {}

    while True:
        queryFromClient = csockid.recv(1024).decode('utf-8')       
        if not queryFromClient:     # if data is not received break
            break
        
        queryFromClient = queryFromClient.rstrip().lower()

        print("Received from client: " + str(queryFromClient))

#send query from client to ts1 and ts2:

        # ts1_Socket.send(queryFromClient.encode('utf-8'))
        # ts2_Socket.send(queryFromClient.encode('utf-8'))


#now ls has to receive data from ts1 and ts2: >>>>>>>>>>>>>>>>>>>>>
        #cant just use receive() call will have to use a nonblocking socket or use select() system call 
        
        #1: receives from ts1
        #2. receives from ts2
        #3. times out after 5 sec bc it didnt receive anything
        
        # declare two empty dictionaries, one for ts1 and one for ts2
        # dict_ts1 = {}
        # dict_ts2 = {}
        # ts = 1
        received_msg=""
        print( ts )
        if queryFromClient in dict_ts1.keys():
            # then we can send to ts1 again
            print( 'in dictionary for ts1' )
            ts1_Socket.sendall(queryFromClient.encode('utf-8'))
        elif queryFromClient in dict_ts2.keys():
            # then we can send to ts2 again
            print( 'in dictionary for ts2' )
            ts2_Socket.sendall(queryFromClient.encode('utf-8'))
        else:
            # decide whether we want to send to ts1 or ts2
            # if ts is 1 then send to ts1 if 2 send to ts2 
            print( 'in neither dictionary' )
            if ts == 1:
                # send to ts1
                dict_ts1[queryFromClient] = 'ts1' # put the query Key in the dict for ts1
                # print( dict_ts1 )
                ts1_Socket.sendall(queryFromClient.encode('utf-8'))
                ts = 2
            elif ts == 2:
                # send to ts2
                dict_ts2[queryFromClient] = 'ts2' # put the query key in the dict for ts2
                ts2_Socket.sendall(queryFromClient.encode('utf-8'))
                ts = 1
        
        # received_msg=""

        '''try:
            ts1_Socket.sendall(queryFromClient.encode('utf-8'))
            print("sent to ts1")
            received_msg= str(ts1_Socket.recv(1024).decode('utf-8'))
            print("received from ts1: " + received_msg)
        
        except mysoc.timeout as e:
            print (e, "Not in ts1")

        try:
            ts2_Socket.sendall(queryFromClient.encode('utf-8'))
            print("sent to ts2")
            received_msg=str(ts2_Socket.recv(1024).decode('utf-8'))
            print("received from ts2: " + received_msg)
            
        except mysoc.timeout as e:
            print (e, "Not in ts2")'''

        if received_msg == "":
            send_msg = queryFromClient + " - Error:HOST NOT FOUND"
            csockid.send(send_msg.encode('utf-8'))
        
        else:
            print("sending to client")
            csockid.send(received_msg.encode('utf-8'))



   # Close the server socket
    clientSocket.close()
    ts1_Socket.close()
    ts2_Socket.close()
    exit()



t1 = threading.Thread(name='server', target=server)
t1.start()

exit()

'''HOST = socket.gethostname() # get the name of the machine that is the host

PORT = int( argv[1] ) #get the port arg and convert it into an int

s = socket.socket( socket.AF_INET, socket.SOCK_STREAM ) # creating the server socket
s.bind( (HOST, PORT) )
s.listen(1) #listens for 1 connection
conn, addr = s.accept()
print( 'Connected by, ', addr ) # prints where the connection came from
while True:
    data = conn.recv(1024) #receives the Key from the Client
    if not data:
        break
    print( data )
conn.close()'''