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
        self.__drawing_canvas = DrawingCanvas(self,width//2,height-40,event_root = root)
        self.__tree_canvas = TreeCanvas(self,width//2,height-40)
        self.__control_bar = Button_Bar(self)
        self.__goal_label = Label(self,text = "Goal path :")
        self.__T = Text(self,height = 1,width=2,padx=10,pady=10)
        self.__T.insert(END, "Goal path will appear here")
        self.__T.config(state=DISABLED)
        self.__H_label = Label(self,text = "Weight or Heurastic : ")
        self.__H_text = Text(self,height = 1,width=2,padx=10,pady=10)
        self.__H_text.insert(END, "weight (Line) , Heurastic(Node)")
        self.__H_text.config(state=DISABLED)
        self.__Name_label = Label(self,text = "Change Node Name :")
        self.__Name_text = Text(self,height = 1,width=2,padx=10,pady=10)
        self.__Name_text.insert(END, "Change node name")
        self.__Name_text.config(state=DISABLED)   
        self.pack_on_screen()
        
        
    def pack_on_screen(self):
        
        self.__goal_label.grid(row=0,column=0,sticky = "NSEW",padx=(0, 5))
        self.__T.grid(row=1,column=0,sticky = "NSEW",padx=(0, 5))
        self.__Name_label.grid(row=0,column=1,sticky = "NSEW",padx=(0, 5))
        self.__Name_text.grid(row=1,column=1,sticky = "NSEW",padx=(0, 5))
        self.__H_label.grid(row=0,column=2,sticky = "NSEW")
        self.__H_text.grid(row=1,column=2,columnspan=2,sticky = "NSEW")
        self.__tree_canvas.grid(row=2,column=0,sticky = "NSEW")
        self.__drawing_canvas.grid(row=2,column=1,columnspan=2,sticky = "NSEW")
        self.__control_bar.grid(row=2,column=3,sticky = "NSEW")
        self.__button = Button(self ,text="breadth search first" , command=self.breadth_search_first)
        self.__button.grid(row=3,column=0,columnspan=3,sticky = "NSEW")
    
    def breadth_search_first(self):
        if self.__drawing_canvas.initial_node:
            initial_node = TreeNode(self.__tree_canvas.canvas,0,None,0,self.width//2,self.__drawing_canvas.initial_node)
            self.__current_thread = BreadthSearchFirst(initial_node,self.goal_set)
            self.__current_thread.start()
    
    def goal_set(self,string):
        
        self.__T.config(state=NORMAL)
        self.__T.delete("1.0","end")
        self.__T.insert(END, string)
        self.__T.config(state=DISABLED)

if __name__ == "__main__":
    
    root =  Tk()
    root.geometry("1000x720")

    can = MainCanvas(root,920,720)
    
    can.grid(row=0,column=0)
    

    root.mainloop()
