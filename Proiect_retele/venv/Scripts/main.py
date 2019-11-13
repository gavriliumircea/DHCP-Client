import socket;
import json

Messages_dictionary={
    "DHCPDISCOVER":1,
    "DHCPOFFER":2,
    "DHCPREQUEST":3,
    "DHCPDECLINE":4,
    "DHCPACK":5,
    "DHCPNAK":6,
    "DHCPRELEASE":7,
    "DHCPINFORM":8
}

Client_States_Dictionary={1:"initial",2:"waiting for DHCPOFFER",3:"sending DHCP request", 4:"Waiting for DHCPACK", 5:"Complete", 6:"Realese IP address",7:"closed"}


class DHCP_Client:
    STATE=1;
    IP_ADDRESS="127.0.0.1"
    UDP_PORT=68

UDP_PORT_TO_TRANSMIT = 67;
MESSAGE = { "type": "1"}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
message_from_server=0
bufferSize= 1024
client=DHCP_Client()
sock.bind((client.IP_ADDRESS,client.UDP_PORT))
while(Client_States_Dictionary[client.STATE]!="closed"):
    if client.STATE==1:
            print("am trimis")
            sock.sendto(json.dumps(MESSAGE).encode(), ('<broadcast>', 67))
            client.STATE=2
    elif client.STATE==2:
        print("asteptam")
        msg=sock.recvfrom(1024)
        print(msg[0])
        client.STATE=3
    elif client.STATE == 3:
        client.STATE=4
    elif client.STATE == 4:
        client.STATE = 5
    elif client.STATE == 5:
        client.STATE = 6
    elif client.STATE == 6:
        client.STATE = 7
    elif client.STATE == 7:
        client.STATE = 8
print("am iesit din while")


