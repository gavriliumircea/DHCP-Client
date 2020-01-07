import socket

message_size=int(225)

Client_States_Dictionary={1:"initial",2:"waiting for DHCPOFFER",3:"sending DHCP request", 4:"Waiting for DHCPACK", 5:"Complete", 6:"Realese IP address",7:"closed"}

class DHCP_Client:
    STATE=1
    IP_ADDRESS="127.0.0.1"
    UDP_PORT=68

class Logger:
    def __init__(self):
        self.f = open("logging.txt", "a+")
    def writeInfo(self, text):
        txt="[Info] "+str(text)+"\n"
        self.f.write(txt)

    def writeError(self, text):
        txt = "[Error] " + str(text)+"\n"
        self.f.write(txt)

    def endCommunication(self):
        self.f.close()

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

def message_factory(type):
    message=bytearray(message_size)
    message[0]=1
    message[1]=1
    message[2]=6
    message[224]=type
    return message

def check_message(message, state):
    if message[0]==2:
        return True
    elif message[224]==state:
        return True
    return False







logger=Logger()
UDP_PORT_TO_TRANSMIT = 67
MESSAGE = "type: 1"
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
message_from_server=0
bufferSize= 1024
client=DHCP_Client()
sock.bind((client.IP_ADDRESS,client.UDP_PORT))
while(Client_States_Dictionary[client.STATE]!="closed"):
    logger.writeInfo("Comunication started")
    if client.STATE==1:
            logger.writeInfo("am starea "+str(client.STATE))
            print("am trimis")
            sock.sendto(message_factory(client.STATE), ('<broadcast>', 67))
            logger.writeInfo("am trimis mesajul de tipul "+str(message_factory(client.STATE)[224]))
            client.STATE=2
    elif client.STATE==2:
        print("asteptam")
        byteArray=sock.recvfrom(1024)
        msg=byteArray[0]
        print(msg[224])
        if check_message(msg,client.STATE)==True:
            print("am primit mesajul de tipul "+str(msg[224]))
#           logger.writeInfo("am starea " +str(client.STATE))
            client.STATE=3
    elif client.STATE == 3:
        print("sunt in starea "+str(client.STATE))
        logger.writeInfo("am starea "+str(client.STATE))
        sock.sendto(message_factory(client.STATE), ('<broadcast>', 67))
        client.STATE=4
    elif client.STATE == 4:
        #logger.writeInfo("am starea "+str(client.STATE))
        print("stare "+ str(client.STATE))
        bytearray=sock.recvfrom(1024)
        msg=bytearray[0]
        print(msg[224])
        if check_message(msg,client.STATE)==True:
            print("am primit mesajul de tipul " + str(msg[224]))
           # client.STATE = 5
    elif client.STATE == 5:
        logger.writeInfo("am starea " + str(client.STATE))
        #client.STATE = 6
    elif client.STATE == 6:
        logger.writeInfo("am starea " +str(client.STATE))
        #client.STATE = 7
    elif client.STATE == 7:
        logger.writeInfo("am starea "+str(client.STATE))
        #client.STATE = 8
    logger.writeInfo("Comunicatie terminata")
print("am iesit din while")
logger.endCommunication()


