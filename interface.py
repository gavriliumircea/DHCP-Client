import tkinter as tk
from main import *
import threading

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        tk.Frame.__init__(self, master)
        self.pack()
        self.master.title("DHCP Client")
        self.client = DHCP_Client()
        self.create_widgets()


    def create_widgets(self):
        self.start_btt = tk.Button(self, text="Start communication", command=self.start)
        self.start_btt.pack()
        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.destroy)
        self.quit.place(x=201, y=50)

        self.var1 = tk.IntVar()
        self.chk1=tk.Checkbutton(self.master, text="Optiunea 53: DHCP message: DHCPDISCOVER", variable=self.var1)
        self.var1.set(1)
        self.var2 = tk.IntVar()
        self.chk2=tk.Checkbutton(self.master, text="Optiunea 50: Requested IP Address", variable=self.var2)

        self.var3 = tk.IntVar()
        self.chk3 = tk.Checkbutton(self.master, text="Optiunea 53: DHCP message: DHCPDISCOVER", variable=self.var3)
        self.var4 = tk.IntVar()
        self.chk4 = tk.Checkbutton(self.master, text="Optiunea 53: DHCP message: DHCPDISCOVER", variable=self.var4)
        self.var5 = tk.IntVar()
        self.chk5 = tk.Checkbutton(self.master, text="Optiunea 53: DHCP message: DHCPDISCOVER", variable=self.var4)

        self.chk1.pack()
        self.chk2.pack()

    def destroy(self):
        #oprire comunicatie
        print("seek and destroy")
        self.client.STATE=7
        self.master.destroy
        exit(0)

    def start(self):
        print("Sending message")
        if(self.var1.get()==0):
            Logger().writeError("Eroare optiune 53")
            self.destroy()
        self.mess=Message(self.var1.get())
        try:
            thread = threading.Thread(target=comm, args=(self.client, self.mess))
            thread.start()
            thread.join()
        except:
            Logger().writeError("Eroare thread")
        self.destroy()


root = tk.Tk()
app = Application(master=root)
app.mainloop()