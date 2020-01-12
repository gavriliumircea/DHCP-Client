import socket
import json




class Message:
    def __init__(self):
        self.message = bytearray(240)
        self.op=2
        # self.XID=random.sample(range(0,255),4)
        self.XID=bytearray([0x18,0x16,0x14,0x12])
        self.message_factory()





    def message_factory(self):
        self.message = bytearray(240)
        self.message[0] = 2
        self.message[1] = 1
        self.message[2] = 6
        self.message[3] = 0
        self.message[4:8] = self.XID
        # message[8:10]                           # secs seconds elapsed since a client began an attempt to acquire or renew a lease.
        self.message[10] = 128    # 128 for broadcast and 0 in rest
        self.message[11] = 0                      # reserved
        self.message[12:16] = [0]*4               # CIAdrr client ip address used ONLY if the client has a valid ip address
        self.message[16:20] = [1]*4           # YIAdrr ip address the server is assigning to the client
        # message[20:24]                          # SIAdrr server ip address (The sending server always includes its own IP address in the Server Identifier DHCP option.)
        # message[24:28]                          # GIAdrr gateway ip address
        # message[28:44]                          # CHAddr client hardware address
        self.message[44:108] = [0]*64             # SName server name The server sending a DHCPOFFER or DHCPACK message may optionally
                                                  # put its name in this field. This can be a simple text “nickname” or a fully-qualified DNS domain name
        self.message[108:236] = [0]*128           # File Optionally used by a client to request a particular type of boot file in a DHCPDISCOVER message.
                                                  # Used by a server in a DHCPOFFER to fully specify a boot file directory path and filename.
        # options

        self.message[236:240]=[99,130,83,99] #magic cookie
        self.message +=bytearray( [53, 1, 2])
        self.message+=bytearray([54, 4, 0, 0, 0, 0])
        self.message += bytearray([1, 4, 255, 255, 255, 0])

         #optiunea 53, len 1, data 1-8
        # # 50 4 req ip address

        self.message+=bytearray([255])
        # # 51 4 req lease time
        # # 54 4 server identifier
        #
        # self.message[message_size-1] = 255
        # self.message.append()
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


UDP_IP = "127.0.0.2"
UDP_PORT = 67
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bufferSize = 1024
sock2.bind((UDP_IP, UDP_PORT))
mesaj = "server"
bytesAddressPair = 0

while True:
    bytesAddressPair = sock2.recvfrom(bufferSize)
    m=Message()
    if (bytesAddressPair != 0):
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        if (message[0] == 1):
            options=unpack(message)
            if 53 in options:
                if options[53]==1:
                    m.message[242]=2
                if options[53]==3:
                    m.message[242]=5
            sock2.sendto(m.message, address)