import socket
import random

message_size = 241

Client_States_Dictionary = {1: "initial", 2: "waiting for DHCPOFFER", 3: "sending DHCP request",
                            4: "Waiting for DHCPACK", 5: "Complete", 6: "Release IP address", 7: "closed"}

Messages_dictionary = {
    "DHCPDISCOVER": 1,
    "DHCPOFFER": 2,
    "DHCPREQUEST": 3,
    "DHCPDECLINE": 4,
    "DHCPACK": 5,
    "DHCPNAK": 6,
    "DHCPRELEASE": 7,
    "DHCPINFORM": 8
}


class DHCP_Client:
    def __init__(self):
        self.STATE = 1
        self.IP_ADDRESS = "127.0.0.1"
        self.UDP_PORT = 68


class Logger:
    def __init__(self):
        self.f = open("logging.txt", "a+")

    def writeInfo(self, text):
        txt = "[Info] " + str(text) + "\n"
        self.f.write(txt)

    def writeError(self, text):
        txt = "[Error] " + str(text) + "\n"
        self.f.write(txt)

    def endCommunication(self):
        self.f.close()

class Message:
    def __init__(self,type):
        self.message = bytearray(message_size)
        self.type=type
        self.op=1
        self.XID=random.sample(range(0,255),4)
        self.message_factory()

    def setFlag(self,type):
        if type in range(3):
            return 128
        else:
            return 0

    def message_factory(self):
        self.message = bytearray(message_size)
        self.message[0] = self.op
        self.message[1] = 1
        self.message[2] = 6
        self.message[3] = 0
        self.message[4:8] = self.XID                       # XID transaction identifier
        # message[8:10]                      # secs seconds elapsed since a client began an attempt to acquire or renew a lease.
        self.message[10] = self.setFlag(type)              # 128 for broadcast and 0 in rest
        self.message[11] = 0                      # reserved
        self.message[12:16] = [0]*4               # CIAdrr client ip address used ONLY if the client has a valid ip address
        self.message[16:20] = [0]*4               # YIAdrr ip address the server is assigning to the client
        # message[20:24]                     # SIAdrr server ip address (The sending server always includes its own IP address in the Server Identifier DHCP option.)
        # message[24:28]                     # GIAdrr gateway ip address
        # message[28:44]                     # CHAddr client hardware address
        self.message[44:108] = [0]*64             # SName server name The server sending a DHCPOFFER or DHCPACK message may optionally
                                             # put its name in this field. This can be a simple text “nickname” or a fully-qualified DNS domain name
        self.message[108:236] = [0]*128           # File Optionally used by a client to request a particular type of boot file in a DHCPDISCOVER message.
                                             # Used by a server in a DHCPOFFER to fully specify a boot file directory path and filename.
        # options
        self.message[237:240] = [53,1,self.type] #optiunea 53, len 1, data 1
        self.message[message_size-1] = 255
        print(self.XID)


    @staticmethod
    def check_message(message,state):
        if message[0] == 2:
            return True
        elif message[message_size - 1] == state:
            return True
        return False


def comm(client):
    logger = Logger()
    UDP_PORT_TO_TRANSMIT = 67
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    bufferSize = 1024
    sock.bind((client.IP_ADDRESS, client.UDP_PORT))
    mess = Message(1)
    while (Client_States_Dictionary[client.STATE] != "closed"):
        if client.STATE == 1:
            logger.writeInfo("Comunication started")
            logger.writeInfo("am starea " + str(client.STATE))
            print("am trimis")
            sock.sendto(mess.message, ('<broadcast>', UDP_PORT_TO_TRANSMIT))
            # logger.writeInfo("am trimis mesajul de tipul " + str(Messages_dictionary[client.STATE]))
            client.STATE = 2
        elif client.STATE == 2:
            print("asteptam")
            response = sock.recvfrom(bufferSize)
            print(Message.check_message(response[0],client.STATE))
            if Message.check_message(response[0],client.STATE) is True:
                print("am primit mesajul de tipul " + str(client.STATE))
                client.STATE = 3
        elif client.STATE == 3:
            print("sunt in starea " + str(client.STATE))
            logger.writeInfo("am starea " + str(client.STATE))
            mess.type=client.STATE
            mess.message_factory()
            sock.sendto(mess.message, ('<broadcast>', UDP_PORT_TO_TRANSMIT))
            client.STATE = 4
        elif client.STATE == 4:
            logger.writeInfo("am starea "+str(client.STATE))
            print("sunt in starea " + str(client.STATE))
            response = sock.recvfrom(bufferSize)
            if Message.check_message(response[0],client.STATE) is True:
                print("am primit mesajul de tipul " + str(client.STATE))
            client.STATE = 7

            # client.STATE = 1
        # elif client.STATE == 5:
        #     logger.writeInfo("am starea " + str(client.STATE))
        #     # client.STATE = 6
        # elif client.STATE == 6:
        #     logger.writeInfo("am starea " + str(client.STATE))
        #     # client.STATE = 7
        elif client.STATE == 7:
            logger.writeInfo("am starea " + str(client.STATE))
    logger.writeInfo("Comunicatie terminata")
    print("am iesit din while")
    logger.endCommunication()
    sock.close()
