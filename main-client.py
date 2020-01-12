import socket
import random
import tkinter as tk
import time


var=1
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
        self.IP_ADDRESS = [127,0,0,1]
        self.IP_ADDRESS_TO_REQUEST = [127, 0, 0, 1]
        self.UDP_PORT = 68
        self.previousIPDictionary={}
        self.serverIP=""
        self.dns=""
        self.mask=""
        self.router=""

    def ipToString(self):
        formated=str(self.IP_ADDRESS[0])+"."+str(self.IP_ADDRESS[1])+"."+str(self.IP_ADDRESS[2])+"."+str(self.IP_ADDRESS[3])
        return formated

    def updateInfo(self,options,message):
        self.IP_ADDRESS[0]=message[16]
        self.IP_ADDRESS[1] = message[17]
        self.IP_ADDRESS[2] = message[18]
        self.IP_ADDRESS[3] = message[19]
        self.previousIPDictionary[self.serverIP]=self.IP_ADDRESS
        if 1 in options:
            self.mask=options[1]
        if 6 in options:
            self.dns=options[6]
        if 3 in options:
            self.router=options[3]


class Logger:
    def __init__(self):
        self.f = open("logging.txt", "a+")
        self.f.write("\n######\n")

    def writeInfo(self, text):
        txt = "[Info] " + str(text) + "\n"
        self.f.write(txt)

    def writeError(self, text):
        txt = "[Error] " + str(text) + "\n"
        self.f.write(txt)

    def endCommunication(self):
        self.f.close()

class Message:
    def __init__(self,type,options):
        self.message = bytearray(240)
        self.type=type
        self.op=1
        # self.XID=random.sample(range(0,255),4)
        self.XID=bytearray([0x18,0x16,0x14,0x22])
        self.options = options
        self.message_factory()



    def setFlag(self,type):
        if type in range(3):
            return 128
        else:
            return 0

    def message_factory(self):
        self.message = bytearray(240)
        self.message[0] = self.op
        self.message[1] = 1
        self.message[2] = 6
        self.message[3] = 0
        self.message[4:8] = self.XID
        # message[8:10]                           # secs seconds elapsed since a client began an attempt to acquire or renew a lease.
        self.message[10] = self.setFlag(self.type)     # 128 for broadcast and 0 in rest
        self.message[11] = 0                      # reserved
        self.message[12:16] = [0]*4               # CIAdrr client ip address used ONLY if the client has a valid ip address
        self.message[16:20] = [0]*4               # YIAdrr ip address the server is assigning to the client
        # message[20:24]                          # SIAdrr server ip address (The sending server always includes its own IP address in the Server Identifier DHCP option.)
        # message[24:28]                          # GIAdrr gateway ip address
        # message[28:44]                          # CHAddr client hardware address
        self.message[44:108] = [0]*64             # SName server name The server sending a DHCPOFFER or DHCPACK message may optionally
                                                  # put its name in this field. This can be a simple text “nickname” or a fully-qualified DNS domain name
        self.message[108:236] = [0]*128           # File Optionally used by a client to request a particular type of boot file in a DHCPDISCOVER message.
                                                  # Used by a server in a DHCPOFFER to fully specify a boot file directory path and filename.
        # options

        self.message[236:240]=[99,130,83,99] #magic cookie
        self.message +=bytearray( [53, 1, self.type])
        self.message+=self.options
         #optiunea 53, len 1, data 1-8
        # # 50 4 req ip address
        # self.message[243:249]=[50,4,192,14,0,3]
        # # 51 4 req lease time
        # # 54 4 server identifier
        #
        # self.message[message_size-1] = 255
        # self.message.append()


    @staticmethod
    def check_message(message,state,options):
        if len(message)<243:
            return False
        if message[0] == 2 and options[53]==state:
            return True

        return False


def formatOptionData(optionNumber,data):
    if optionNumber==54 or optionNumber==1:
        ipAddress=""
        ipAddress+=str(data[0])+"."+str(data[1])+"."+str(data[2])+"."+str(data[3])
        return  ipAddress
    if optionNumber==6:
        return  data.decode('utf-8')
    return int.from_bytes(data,"big")


def unpack(message):
    dict={}
    index=240
    while index<len(message)-1:
        optionNumber=message[index]
        optionLength=message[index+1]
        optionData=message[index+2:index+optionLength+2]
        index=index+optionLength+2
        dict[optionNumber]=formatOptionData(optionNumber,optionData)

    return dict




def comm(client,mess,widget):
    logger = Logger()
    UDP_PORT_TO_TRANSMIT = 67
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    bufferSize = 1024
    sock.bind((client.ipToString(), client.UDP_PORT))


    while (Client_States_Dictionary[client.STATE] != "closed"):
        if client.STATE == 1:
            logger.writeInfo("Comunication started")
            logger.writeInfo("am starea " + str(client.STATE))
            print("am trimis discover")
            widget.insert(tk.INSERT,"am trimis discover")
            widget.update_idletasks()
            sock.sendto(mess.message, ('<broadcast>', UDP_PORT_TO_TRANSMIT))
            # logger.writeInfo("am trimis mesajul de tipul " + str(Messages_dictionary[client.STATE]))
            client.STATE = 2

        elif client.STATE == 2:
            print("asteptam")
            widget.insert(tk.INSERT, "\nasteptam")
            widget.update_idletasks()
            response = sock.recvfrom(bufferSize)
            # print(Message.check_message(response[0],client.STATE))
            serverOptions=unpack(response[0])
            if Message.check_message(response[0],client.STATE,serverOptions) is True:
                print("am primit mesajul de tipul " + str(client.STATE))
                widget.insert(tk.INSERT, "\nam primit mesajul de tipul " + str(client.STATE))
                widget.update_idletasks()
                if 54 in serverOptions:
                    client.serverIP=serverOptions[54]
                    if client.serverIP in client.previousIPDictionary:
                       client.IP_ADDRESS_TO_REQUEST=client.previousIPDictionary[client.serverIP]
                client.STATE = 3

        elif client.STATE == 3:
            print("sunt in starea " + str(client.STATE))
            widget.insert(tk.INSERT, "\nsunt in starea " + str(client.STATE))
            widget.update_idletasks()
            logger.writeInfo("am starea " + str(client.STATE))
            mess.type=client.STATE
            mess.message_factory()
            sock.sendto(mess.message, ('<broadcast>', UDP_PORT_TO_TRANSMIT))
            client.STATE = 4

        elif client.STATE == 4:
            logger.writeInfo("am starea "+str(client.STATE))
            widget.insert(tk.INSERT, "\nam starea "+str(client.STATE))
            widget.update_idletasks()
            print("sunt in starea " + str(client.STATE))
            response = sock.recvfrom(bufferSize)
            serverOptions = unpack(response[0])
            if Message.check_message(response[0],5,serverOptions) is True:
                print("am primit mesajul de tipul " + str(client.STATE))
                client.updateInfo(serverOptions,response[0])
                print("ip address "+str(client.IP_ADDRESS))
                print(client.mask)
                print(client.previousIPDictionary)
                print(client.serverIP)
                widget.insert(tk.INSERT, "\nam primit mesajul de tipul " + str(client.STATE))
                widget.insert(tk.INSERT, "\nip address: " + str(client.IP_ADDRESS))
                widget.insert(tk.INSERT, "\nmask: " + client.mask)
                widget.insert(tk.INSERT, "\npreviousIPDictionary: " + str(client.previousIPDictionary))
                widget.insert(tk.INSERT, "\nserver IP: " + client.serverIP)
                widget.update_idletasks()
                client.STATE=5
            elif Message.check_message(response[0],6,serverOptions) is True:
                print("am primit mesajul de tipul nack")
                widget.insert(tk.INSERT, "\nam primit mesajul de tipul nack")
                widget.update_idletasks()
                client.STATE=3
        elif client.STATE == 5:

            logger.writeInfo("set up complete waiting for user to release and close " )

        elif client.STATE == 6:
            logger.writeInfo("sending release " )
            widget.insert(tk.INSERT, "\nsending release ")
            widget.update_idletasks()
            print("sending release ")
            client.STATE=7
            mess.type = client.STATE
            mess.message_factory()
            sock.sendto(mess.message, ('<broadcast>', UDP_PORT_TO_TRANSMIT))
    logger.writeInfo("Comunicatie terminata")
    widget.insert(tk.INSERT, "\nComunicatie terminata")
    widget.update_idletasks()
    print("am iesit din while")
    logger.endCommunication()
    sock.close()
