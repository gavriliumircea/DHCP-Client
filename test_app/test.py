
class Message:
    def __init__(self):
        self.message = bytearray(240)
        self.op=1
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
        self.message +=bytearray( [53, 1, 2])
        self.message+=bytearray([54, 4, 0, 0, 0, 0])

         #optiunea 53, len 1, data 1-8
        # # 50 4 req ip address
        self.message+=bytearray([50,1,3])
        # # 51 4 req lease time
        # # 54 4 server identifier
        #
        # self.message[message_size-1] = 255
        # self.message.append()

def formatOptionData(optionNumber,data):
    if optionNumber==54 or 1:
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


mesaj=Message()
print(unpack(mesaj.message))