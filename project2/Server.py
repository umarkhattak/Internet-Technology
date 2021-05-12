import argparse
from sys import argv
import socket

import struct
import binascii


def send_udp_message(message, address, port): #THIS FUNCTION WAS RECIEVED FROM https://routley.io/posts/hand-writing-dns-messages/
    """send_udp_message sends a message to UDP server

    message should be a hexadecimal encoded string
    """
    message = message.replace(" ", "").replace("\n", "")
    server_address = (address, port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(binascii.unhexlify(message), server_address)
        data, _ = sock.recvfrom(4096)
    finally:
        sock.close()
    return binascii.hexlify(data).decode("utf-8")

def format_hex(hex): # #THIS FUNCTION WAS RECIEVED FROM https://routley.io/posts/hand-writing-dns-messages/
    octets = [hex[i:i+2] for i in range(0, len(hex), 2)]
    pairs = [" ".join(octets[i:i+2]) for i in range(0, len(octets), 2)]
    return "\n".join(pairs)

def create_hex_string( data ):
    decoded = data.decode( 'utf-8' )
    decoded = decoded.split( '.' )
    hex_string = ""
    i = 0
    while i < len(decoded):
        if len(decoded[i]) <= 15:
            hex_string = hex_string + "0" + format(len( decoded[i] ), '0') + decoded[i].encode( 'utf-8' ).hex()
        else:
            hex_string = hex_string + format(len( decoded[i] ), '0') + decoded[i].encode( 'utf-8' ).hex()
        i += 1
    return hex_string

HOST = socket.gethostname() # get the name of the machine that is the host

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

    hex_string = create_hex_string( data )

    hex_string = "AA AA 01 00 00 01 00 00 00 00 00 00 " + hex_string + " 00 00 01 00 01"
    response = send_udp_message( hex_string, '8.8.8.8', 53 )
    print( format_hex( response ) )

    k = (14*4) + 2
    sent = 0
    data_to_send = ""
    while k < len(response):
        if response[k:k+2] == "05":
            if sent == 0:
                data_to_send = "other"
                print("This is an other")
                sent += 1
            
            k+= 50
            
        elif response[k:k+2] == "04":
            ip_address_hex = response[k+2:k+10]
            int_ip = int(ip_address_hex, 16)
            print( socket.inet_ntoa(struct.pack(">L", int_ip)) )
            if sent == 0:
                data_to_send = data_to_send + socket.inet_ntoa(struct.pack(">L", int_ip))
                sent += 1
            else:
                data_to_send = data_to_send + "," + socket.inet_ntoa(struct.pack(">L", int_ip))
                sent += 1

        k += 2

    data_to_send = data_to_send.encode( 'utf-8' )
    conn.sendall(data_to_send)

 
    '''sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto( data, ('8.8.8.8', 5005) )

    sock.bind( ('8.8.8.8', 5005) )'''

    '''while True:
            response, addr = sock.recvfrom(1024)
            print( response )
    if not data:
        break'''

    '''if not data:
        break
    ip_address = socket.gethostbyname_ex( data )
    print( ip_address )
    if type( ip_address[2] ) == list:
        conn.sendall( ip_address[2][0] )
    else:
        conn.sendall( ip_address[2] )'''
conn.close() #close the connection gracefully