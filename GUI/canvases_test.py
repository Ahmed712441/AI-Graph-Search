import sys

sys.path.append("D:\AI\Project")

from tkinter import *
from settings import *
from tkinter.ttk import *
from treecanvas import TreeCanvas
from canvas import DrawingCanvas
from Buttons import Button_Bar
from Algorithms.base_class import BreadthSearchFirst
from treenode import TreeNode


class MainCanvas(Frame):

    def __init__(self,root,width=200,height=200):
        self.width = width
        Frame.__init__(self, root,width=width,height=height) 
        self.__drawing_canvas = DrawingCanvas(self,width//2,height-20,event_root = root)
        self.__tree_canvas = TreeCanvas(self,width//2,height-20)
        self.__control_bar = Button_Bar(self)
        self.__tree_canvas.grid(row=0,column=0,sticky = "NSEW")
        self.__drawing_canvas.grid(row=0,column=1,sticky = "NSEW")
        self.__control_bar.grid(row=0,column=2,sticky = "NSEW")
        self.__button = Button(self ,text="breadth search first" , command=self.breadth_search_first)
        self.__button.grid(row=1,column=0,columnspan=3,sticky = "NSEW")

    def breadth_search_first(self):
        
        initial_node = TreeNode(self.__tree_canvas.canvas,0,None,0,self.width//2,self.__drawing_canvas.initial_node)
        self.__current_thread = BreadthSearchFirst(initial_node)
        self.__current_thread.start()
        

if __name__ == "__main__":
    
    root =  Tk()
    root.geometry("1000x720")

    can = MainCanvas(root,920,720)
    
    can.grid(row=0,column=0)
    # root.columnconfigure(0, weight=1)
    # root.rowconfigure(0, weight=1)
    

    root.mainloop()
