import tkinter as tk
from main import *

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
        self.chk1=tk.Checkbutton(self.master, text="option 1", variable=self.var1)
        self.var2 = tk.IntVar()
        self.chk2=tk.Checkbutton(self.master, text="option 2", variable=self.var2)
        self.chk1.pack()
        self.chk2.pack()

    def destroy(self):
        #oprire comunicatie
        self.client.STATE=7
        self.master.destroy
        exit(0)

    def start(self):
        print("Sending message")
        print(self.var1.get(),self.var2.get())
        comm(self.client)
        self.destroy()

root = tk.Tk()
app = Application(master=root)
app.mainloop()