import threading
import time
import random
import socket as mysoc_TS2
import sys


def server():
    try:
        ss=mysoc_TS2.socket(mysoc_TS2.AF_INET, mysoc_TS2.SOCK_STREAM)
        print("[S]: Server socket created")
    except mysoc_TS2.error as err:
        print('{} \n'.format("socket open error ",err))
    input_sys = sys.argv
    ts2Port = int(input_sys[1])    
    server_binding=('',ts2Port)
    ss.bind(server_binding)
    ss.listen(10)

    host=mysoc_TS2.gethostname()

    print("[S]: Server host name is: ",host)
    localhost_ip=(mysoc_TS2.gethostbyname(host))
    print("[S]: Server IP address is  ",localhost_ip)
   
 
    csockid,addr=ss.accept()
    print ("[S]: Got a connection request from a client at", addr)

    
    ts2_file = open("PROJ3-HNS.txt", "r")
    ts2_dict = {}

    for line in ts2_file:
        y = line.split()
        ts2_dict[y[0]] = y[1:] 

    ts2_file.close()
    print(ts2_dict)


    while True:
        '''try:
            data = csockid.recv(1024).decode('utf-8')   
            print(data)    
        except mysoc_TS2.error as err:
            print('{} \n'.format("socket send error ",err))'''

        data = csockid.recv(1024).decode('utf-8')
        if not data:     # if data is not received break
            break
        print( data )
        
        '''data = data.rstrip().lower()

        if data in ts2_dict:
            y = ts2_dict[data]
            ip = y[0]
            flag = y[1]
            new_msg2 = str(data + " " + ip + " " + flag)    
            print(new_msg2)
            csockid.sendall(new_msg2.encode('utf-8'))'''


   # Close the server socket
    ss.close()
    exit()




t1 = threading.Thread(name='server', target=server)
t1.start()
time.sleep(random.random()*5)

exit()