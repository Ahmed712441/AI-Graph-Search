from tkinter import *
from settings import *

class TreeCanvas(Frame):

    def __init__(self,root,width=200,height=200,canvas_width=1000,canvas_height=1000):
        
        Frame.__init__(self, root,width=width,height=height) 
        self.count_nodes = 0 # this variable used to count nodes helpful in labeling nodes
        self.hor_scrollbar = Scrollbar(self, orient=HORIZONTAL)
        self.ver_scrollbar = Scrollbar(self, orient=VERTICAL)
        self.canvas = Canvas(self,height=height-100,width=width-100,background=CANVAS_BACKGROUND_COLOR,scrollregion=(0, 0, canvas_width, canvas_height),yscrollcommand=self.ver_scrollbar.set,xscrollcommand=self.hor_scrollbar.set) # canvas object
        self.hor_scrollbar['command'] = self.canvas.xview
        self.ver_scrollbar['command'] = self.canvas.yview
        self.grid_propagate(0) # used to assures that frame will take its height and width even its children are smaller
        self.canvas.grid(row=0,column=0,sticky=(N,W,E,S))  # places the canvas in row : 0 , column :0 in the frame
        self.hor_scrollbar.grid(column=0, row=1, sticky=(W,E))
        self.ver_scrollbar.grid(column=1, row=0, sticky=(N,S))
        
    
    def draw_node(self):
        pass





if __name__=="__main__":


    root =  Tk()
    root.geometry("1000x1000")

    can = TreeCanvas(root,500,500)

    can.grid()


    root.mainloop()