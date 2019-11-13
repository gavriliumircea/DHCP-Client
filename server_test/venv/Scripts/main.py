import socket;
import json;
UDP_IP="127.0.0.2";
UDP_PORT = 67;
sock2= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bufferSize=1024;
sock2.bind((UDP_IP, UDP_PORT))
mesaj="server"
bytesAddressPair=0;

while True:
    bytesAddressPair = sock2.recvfrom(bufferSize)
    if(bytesAddressPair!=0):
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        if(message.decode().__contains__('"type": "1"')):
            print("Am primit mesajul: ", message.decode())
            print("de la adresa: ", address)
            sock2.sendto(mesaj.encode(),address)