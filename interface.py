import tkinter as tk
import main as m
import threading



class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        tk.Frame.__init__(self, master)
        self.pack()
        self.master.title("DHCP Client")
        self.client = m.DHCP_Client()
        self.create_widgets()

    def create_widgets(self):
        self.start_btt = tk.Button(self, text="Start communication", command=self.start)
        self.start_btt.pack()
        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.destroy)
        self.quit.place(x=201, y=50)

        self.var1 = tk.IntVar()
        self.chk1 = tk.Checkbutton(self.master, text="Optiunea 53: DHCP message: DHCPDISCOVER", variable=self.var1)
        self.var1.set(1)
        self.var2 = tk.IntVar()
        self.chk2 = tk.Checkbutton(self.master, text="Optiunea 50: Requested IP Address", variable=self.var2)

        self.var3 = tk.IntVar()
        self.chk3 = tk.Checkbutton(self.master, text="Optiunea 51: Request lease time of 30 minutes ",
                                   variable=self.var3)
        self.var4 = tk.IntVar()
        self.chk4 = tk.Checkbutton(self.master, text="Optiunea 54: Server Identifier", variable=self.var4)
        self.var5 = tk.IntVar()
        self.chk5 = tk.Checkbutton(self.master, text="Optiunea 58 ", variable=self.var5)
        self.var6 = tk.IntVar()
        self.chk6 = tk.Checkbutton(self.master, text="Optiunea 61 ", variable=self.var6)
        self.var7 = tk.IntVar()
        self.chk7 = tk.Checkbutton(self.master, text="Optiunea 55 ", variable=self.var7)
        self.var8 = tk.IntVar()
        self.chk8 = tk.Checkbutton(self.master, text="Optiunea 12 ", variable=self.var8)
        self.var9 = tk.IntVar()
        self.chk9 = tk.Checkbutton(self.master, text="Optiunea 15 ", variable=self.var9)

        self.chk1.pack()
        self.chk2.pack()
        self.chk3.pack()
        self.chk4.pack()
        self.chk5.pack()
        self.chk6.pack()
        self.chk7.pack()
        self.chk8.pack()
        self.chk9.pack()

        self.releaseButton=tk.Button(text="Release Ip address",command=self.release)
        self.releaseButton.pack()
        self.text=tk.Text()
        self.text.pack()

    def release(self):

        self.client.STATE=6

    def destroy(self):
        # oprire comunicatie
        print("seek and destroy")
        self.client.STATE = 7
        self.master.destroy
        exit(0)

    def optionBuilder(self):
        options = bytearray()
        if (self.var2.get()):
            options += bytearray([50, 4, self.client.IP_ADDRESS_TO_REQUEST[0], self.client.IP_ADDRESS_TO_REQUEST[1], self.client.IP_ADDRESS_TO_REQUEST[2], self.client.IP_ADDRESS_TO_REQUEST[3]])
        if (self.var3.get()):
            options += bytearray([51, 4, 0, 0, 0x07, 0x08])
            # options+='0x00'
        if (self.var4.get()):
            options += bytearray([54, 4, 0, 0, 0, 0])
        if(self.var5.get()):
            options+=bytearray([58,4,0,0,0x01,0xc2])
        if(self.var6.get()):
            # 0a0027000035
            options+=bytearray([61,7,1,0x0a,0x00,0x27,0x00,0x00,0x35])
        if(self.var7.get()):
            options+=bytearray([55,3,1,3,6])
        if(self.var8.get()):
            options+=bytearray([12,6])
            options.extend((map(ord,"client")))
        if(self.var9.get()):
            options+=bytearray([15,5])
            options.extend((map(ord, "1306A")))

        options = options + bytearray([255])
        return options

    def start(self):
        print("Sending message")
        if (self.var1.get() == 0):
            m.Logger().writeError("Eroare optiune 53")
            self.destroy()
        self.mess = m.Message(1, self.optionBuilder())
        try:
            thread2 = threading.Thread(target=m.comm, args=(self.client, self.mess,self.text))
            # thread2 = threading.Thread(target=self.release)
            thread2.start()
            # thread2.start()
            # thread2.join()
        except:
            m.Logger().writeError("Eroare thread")
        # comm(self.client,self.mess)
        # self.destroy()


root = tk.Tk()
app = Application(master=root)
app.mainloop()

