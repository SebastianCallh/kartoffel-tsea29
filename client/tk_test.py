from tkinter import *
import threading
import time
import bt_test_client


class BT_client(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
        
    def run(self):
        print("kör mainloop...")
        bt_test_client.main()

class gui:

    def __init__(self):
        self.color = "blue"
        self.maxlistitem = 3
        self.currentitems = 0
        self.root = Tk()
        self.w = Canvas(self.root,width=300,height=300)
        self.w.pack()
        self.listb = Listbox(self.root)
        self.listb.pack()

    def drawrect(self):
        if self.color == "blue":
            self.color = "red"
        else:
            self.color = "blue"
        self.w.create_rectangle(50,25,150,75,fill=self.color)

    def delay(self):
        time.sleep(2)
        self.drawrect()
        self.listb.insert(END, "hej")
        self.currentitems += 1
        if self.currentitems == self.maxlistitem+1:
            self.currentitems = 0
            self.listb.delete(0, END)
        self.w.after(500,self.delay)
    
    def start(self):
        self.w.after(100,self.delay)
        self.root.mainloop()
    
#bt_client = BT_client()
#bt_client.start()

gui = gui()
gui.start()


