from tkinter import *
from tkinter import ttk

class Content(Frame):
    def __init__(self,root):
        Frame.__init__(self, root) 
        frame = ttk.Frame(self, borderwidth=5, relief="ridge", width=200, height=100)
        namelbl = ttk.Label(self, text="Name")
        name = ttk.Entry(self)

        onevar = BooleanVar()
        twovar = BooleanVar()
        threevar = BooleanVar()

        onevar.set(True)
        twovar.set(False)
        threevar.set(True)

        one = ttk.Checkbutton(self, text="One", variable=onevar, onvalue=True)
        two = ttk.Checkbutton(self, text="Two", variable=twovar, onvalue=True)
        three = ttk.Checkbutton(self, text="Three", variable=threevar, onvalue=True)
        ok = ttk.Button(self, text="Okay")
        cancel = ttk.Button(self, text="Cancel")


        frame.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))
        namelbl.grid(column=3, row=0, columnspan=2, sticky=(N, W), padx=5)
        name.grid(column=3, row=1, columnspan=2, sticky=(N,E,W), pady=5, padx=5)
        one.grid(column=0, row=3)
        two.grid(column=1, row=3)
        three.grid(column=2, row=3)
        ok.grid(column=3, row=3)
        cancel.grid(column=4, row=3)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=3)
        self.columnconfigure(4, weight=3)
        self.rowconfigure(1, weight=1)


if __name__ == "__main__":
    root = Tk()

    content = Content(root)
    content.grid(column=0, row=0, sticky=(N, S, E, W))

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)


    root.mainloop() 


