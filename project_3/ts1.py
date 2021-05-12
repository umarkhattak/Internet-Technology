import threading
import random
import socket as mysoc_TS1
import sys


def server():
    try:
        ss=mysoc_TS1.socket(mysoc_TS1.AF_INET, mysoc_TS1.SOCK_STREAM)
        print("[S]: Server socket created")
    except mysoc_TS1.error as err:
        print('{} \n'.format("socket open error ",err))
    input_sys = sys.argv

    ts1Port = int(input_sys[1])    
    server_binding=('',ts1Port)
    ss.bind(server_binding)
    ss.listen(10)

   
    ls_sockid,addr=ss.accept()
    print ("[S]: Got a connection request from a client at", addr)

    
    ts1_file = open("PROJ3-HNS.txt", "r")
    ts1_dict = {}

    for line in ts1_file:
        y = line.split()
        ts1_dict[y[0]] = y[1:] 

    ts1_file.close()
    print(ts1_dict)


    while True:
        '''try:
            data = ls_sockid.recv(1024).decode('utf-8')  
            print(data)     
        except mysoc_TS1.error as err:
            print('{} \n'.format("socket send error ",err))'''

        data = ls_sockid.recv(1024).decode('utf-8')
        if not data:     # if data is not received break
            break
        print( data )
        '''data = data.rstrip().lower()

        if data in ts1_dict:
            y = ts1_dict[data]
            ip = y[0]
            flag = y[1]
            new_msg2 = str(data + " " + ip + " " + flag)    
            print(new_msg2)
            ls_sockid.send(new_msg2.encode('utf-8'))'''


   # Close the server socket
    ss.close()
    exit()



   
t1 = threading.Thread(name='server', target=server)
t1.start()

exit()