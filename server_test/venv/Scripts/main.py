import socket;
import json;

message_size=225

def message_factory(type):
    message=bytearray(message_size)
    message[0]=2;
    message[1]=1;
    message[2]=6;
    message[224]=type;
    return message

UDP_IP="127.0.0.2";
UDP_PORT = 67;
sock2= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bufferSize=1024;
sock2.bind((UDP_IP, UDP_PORT))
mesaj="server"
bytesAddressPair=0

while True:
    bytesAddressPair = sock2.recvfrom(bufferSize)
    if(bytesAddressPair!=0):
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        if(message[0]==1):
            rcv_msg_type=message[224]
            print("Am primit mesajul: ", message[224])
            print("de la adresa: ", address)
            print(message_factory(rcv_msg_type + 1)[224])
            sock2.sendto(message_factory(rcv_msg_type+1),address)