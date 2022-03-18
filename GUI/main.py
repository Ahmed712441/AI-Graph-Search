from tkinter import *

from Buttons import Button_Bar

root = Tk()

control = Button_Bar(root)


control.grid(column=0,row=0)





root.mainloop()
# root =  Tk()
# root.geometry("500x500")
# sidebar =  Frame(root,width=100,height=500,padx=10,bg="#000")

# canvas =  Frame(root,width=300,height=500,padx=10,bg="#fff")

# drawings =  Frame(root,width=100,height=100,padx=10,bg="#0ff")


# sidebar.grid(column=0,row=0)
# canvas.grid(column=1,row=0)
# drawings.grid(column=2,row=0)


# root.columnconfigure(1, weight=1)
# root.rowconfigure(0, weight=1)

# 


