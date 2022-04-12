import sys

sys.path.append("D:\AI\Project")

from tkinter import *
from settings import *
from tkinter.ttk import *
from treecanvas import TreeCanvas
from canvas import DrawingCanvas
from Buttons import *
from Algorithms.base_class import BreadthSearchFirst,DepthFirstSearch
from treenode import TreeNode
from utils import mouse , Mouse_state

class MainCanvas(Frame):

    def __init__(self,root,width=200,height=200):
        self.width = width
        Frame.__init__(self, root,width=width,height=height) 
        self.__drawing_canvas = DrawingCanvas(self,width//2,height-120,event_root = root)
        self.__delete_canvas_button = Button_Bar.create_button(self,os.path.join(os.getcwd(),'GUI','images','delete_icon.png'),self.__drawing_canvas.delete_all)
        self.__tree_canvas = TreeCanvas(self,width//2,height-120)
        self.__control_bar = Button_Bar(self)
        self.__buttons = InteractionButtons(self,self.pause_callback,self.resume_callback,self.terminate_callback,self.delete_all)
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
        self.__button = Button(self ,text="breadth search first" , command=self.breadth_search_first)
        self.__current_thread = None   
        self.pack_on_screen()
    


    def pack_on_screen(self):
        
        self.__goal_label.grid(row=0,column=0,sticky = "NSEW",padx=(0, 5))
        self.__T.grid(row=1,column=0,sticky = "NSEW",padx=(0, 5))
        self.__Name_label.grid(row=0,column=1,sticky = "NSEW",padx=(0, 5))
        self.__Name_text.grid(row=1,column=1,sticky = "NSEW",padx=(0, 5))
        self.__H_label.grid(row=0,column=2,sticky = "NSEW")
        self.__H_text.grid(row=1,column=2,sticky = "NSEW")
        self.__tree_canvas.grid(row=2,column=0,sticky = "NSEW")
        self.__drawing_canvas.grid(row=2,column=1,columnspan=2,sticky = "NSEW")
        self.__control_bar.grid(row=2,column=3,sticky = "NSEW")
        self.__buttons.grid(row=3,column=0)
        self.__delete_canvas_button.grid(row=3,column=1)
        self.__button.grid(row=4,column=0,columnspan=3,sticky = "NSEW")
        self.columnconfigure(0,weight=2)
        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=1)
        self.rowconfigure(2,weight=1)
        
        

    def pause_callback(self):
        if self.__current_thread :
            self.__current_thread.pause()
            self.__buttons.pause.config(state=DISABLED)
            self.__buttons.resume.config(state=NORMAL)
    
    def resume_callback(self):
        if self.__current_thread :
            self.__current_thread.resume()
            self.__buttons.pause.config(state=NORMAL)
            self.__buttons.resume.config(state=DISABLED)
    
    def terminate_callback(self):
        if self.__current_thread :
            self.__current_thread.stop()
            self.thread_finish()

    def delete_all(self):
        self.__tree_canvas.canvas.delete("all")
        self.__buttons.delete.config(state=DISABLED)
        self.__T.config(state=NORMAL)
        self.__T.delete("1.0","end")
        self.__T.insert(END, "Goal path will appear here")
        self.__T.config(state=DISABLED)
        self.__drawing_canvas.reset()
        self.__control_bar.enable()

    def thread_finish(self):
        self.__buttons.pause.config(state=DISABLED)
        self.__buttons.resume.config(state=DISABLED)
        self.__buttons.terminate.config(state=DISABLED)
        self.__buttons.delete.config(state=NORMAL)
        self.__current_thread = None
        
    
    
    def breadth_search_first(self):
        if self.__drawing_canvas.initial_node and not self.__current_thread:
            initial_node = TreeNode(self.__tree_canvas.canvas,0,None,0,self.__tree_canvas.canvas.winfo_width(),self.__drawing_canvas.initial_node)
            self.__current_thread = DepthFirstSearch(initial_node,self.goal_set,self.goal_notfound)
            self.__current_thread.start()
            self.__buttons.pause.config(state=NORMAL)
            self.__buttons.terminate.config(state=NORMAL)
            self.__control_bar.disable()    

    
    def goal_set(self,string):
        
        self.__T.config(state=NORMAL)
        self.__T.delete("1.0","end")
        self.__T.insert(END, string)
        self.__T.config(state=DISABLED)
        self.thread_finish()
    
    def goal_notfound(self):
        
        self.__T.config(state=NORMAL)
        self.__T.delete("1.0","end")
        self.__T.insert(END,"Goal wasnot found")
        self.__T.config(state=DISABLED)
        self.thread_finish()

if __name__ == "__main__":
    
    root =  Tk()
    root.geometry("1000x720")

    can = MainCanvas(root,920,720)
    
    can.grid(row=0,column=0,sticky = "NSEW")
    
    root.columnconfigure(0,weight=1)
    root.rowconfigure(0,weight=1)

    root.mainloop()
