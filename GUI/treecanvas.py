from tkinter import *
from .settings import *

class TreeCanvas(Frame):

    def __init__(self,root,canvas_width=1000,canvas_height=10000):
        
        Frame.__init__(self, root) 
        self.count_nodes = 0 # this variable used to count nodes helpful in labeling nodes
        self.hor_scrollbar = Scrollbar(self, orient=HORIZONTAL)
        self.ver_scrollbar = Scrollbar(self, orient=VERTICAL) # height=height-20,width=width-20
        self.canvas = Canvas(self,background=CANVAS_BACKGROUND_COLOR,scrollregion=(0, 0, canvas_width, canvas_height),yscrollcommand=self.ver_scrollbar.set,xscrollcommand=self.hor_scrollbar.set) # canvas object
        self.hor_scrollbar['command'] = self.canvas.xview
        self.ver_scrollbar['command'] = self.canvas.yview
        self.pack_on_screen()
    
    def pack_on_screen(self):
        self.canvas.grid(row=0,column=0,sticky=(N,W,E,S))  # places the canvas in row : 0 , column :0 in the frame
        self.hor_scrollbar.grid(column=0, row=1, sticky=(W,E))
        self.ver_scrollbar.grid(column=1, row=0, sticky=(N,S))
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)



if __name__=="__main__":


    root =  Tk()
    can = TreeCanvas(root)

    can.grid(row=0,column=0,sticky=(N, S, E, W))
    root.rowconfigure(0,weight=1)
    root.columnconfigure(0,weight=1)
    

    root.mainloop()