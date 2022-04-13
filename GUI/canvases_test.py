import sys

sys.path.append("D:\AI\Project")

from tkinter import *
from settings import *
from tkinter.ttk import *
from treecanvas import TreeCanvas
from canvas import DrawingCanvas
from Buttons import *
from treenode import TreeNode
from radio_buttons import AlgorithmsRadioButtons
from Node import Line,Node

class MainCanvas(Frame):

    def __init__(self,root,width=200,height=200):
        self.width = width
        Frame.__init__(self, root,width=width,height=height) 
        self.__drawing_canvas = DrawingCanvas(self,width//2,height-120,event_root = root,onselect=self.__on_element_selection,onrelease=self.__on_element_release)
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
        self.__Name_text.bind("<FocusIn>",lambda x: self.__set_focus())
        self.__Name_text.bind("<FocusOut>",lambda x: self.__clear_focus())
        self.__H_text.bind("<FocusIn>",lambda x:  self.__set_focus())
        self.__Name_text.bind("<FocusOut>",lambda x: self.__clear_focus())
        self.__submit_changes = Button(self ,text="Submit Changes" , command=self.__change_node)
        self.__submit_changes.config(state=DISABLED)
        self.__current_thread = None   
        self.__radio_buttons = AlgorithmsRadioButtons(self,self.__submit_callback,self.__drawing_canvas)
        self.__focus = False
        self.__pack_on_screen()
    
    def __set_focus(self):
        self.__focus = True

    def __clear_focus(self):
        self.__focus = False
    
    def get_focus(self):
        return self.__focus

    def __on_element_selection(self):

        if isinstance(self.__drawing_canvas.selected , Line):
            self.__H_text.config(state=NORMAL)
            self.__submit_changes.config(state=NORMAL)
            self.__H_text.delete("1.0","end")
            self.__H_text.insert(END, str(self.__drawing_canvas.selected.get_weight()))
        if isinstance(self.__drawing_canvas.selected , Node):
            self.__Name_text.config(state=NORMAL)
            self.__H_text.config(state=NORMAL)
            self.__submit_changes.config(state=NORMAL)
            self.__H_text.delete("1.0","end")
            self.__Name_text.delete("1.0","end")
            self.__H_text.insert(END, str(self.__drawing_canvas.selected.get_heurastic()))
            self.__Name_text.insert(END, str(self.__drawing_canvas.selected.get_label()))
            
    
    def __on_element_release(self):
        
        self.__clear_focus()
        self.__H_text.delete("1.0","end")
        self.__Name_text.delete("1.0","end")
        self.__Name_text.insert(END, "Change node name")
        self.__H_text.insert(END, "weight (Line) , Heurastic(Node)")
        self.__H_text.config(state=DISABLED)
        self.__submit_changes.config(state=DISABLED)
        self.__Name_text.config(state=DISABLED)
        

    def __change_node(self):
        if isinstance(self.__drawing_canvas.selected , Line):
            self.__drawing_canvas.selected.set_weight(int(self.__H_text.get("1.0", "end-1c")))
        elif isinstance(self.__drawing_canvas.selected , Node):
            self.__drawing_canvas.selected.set_heurastic(int(self.__H_text.get("1.0", "end-1c")))
            self.__drawing_canvas.selected.set_label(self.__Name_text.get("1.0", "end-1c"))
    
    def __submit_callback(self,thread_class,**kwargs):

        if self.__drawing_canvas.initial_node and not self.__current_thread:
            initial_node = TreeNode(self.__tree_canvas.canvas,0,None,0,self.__tree_canvas.canvas.winfo_width(),self.__drawing_canvas.initial_node)
            self.__current_thread = thread_class(initial_node,self.__goal_set,self.__goal_notfound,**kwargs)
            self.__current_thread.start()
            self.__buttons.pause.config(state=NORMAL)
            self.__buttons.terminate.config(state=NORMAL)
            self.__control_bar.disable()    


    def __pack_on_screen(self):
        
        
        self.__goal_label.grid(row=0,column=1,sticky = "NSEW",padx=(0, 5))
        self.__T.grid(row=1,column=1,sticky = "NSEW",padx=(0, 5))
        self.__Name_label.grid(row=0,column=2,sticky = "NSEW",padx=(0, 5))
        self.__Name_text.grid(row=1,column=2,sticky = "NSEW",padx=(0, 5))
        self.__H_label.grid(row=0,column=3,sticky = "NSEW")
        self.__H_text.grid(row=1,column=3,sticky = "NSEW")
        self.__submit_changes.grid(row=1,column=4,sticky = "NSEW",padx=(5, 0))
        self.__tree_canvas.grid(row=2,column=1,sticky = "NSEW")
        self.__drawing_canvas.grid(row=2,column=2,columnspan=2,sticky = "NSEW")
        self.__control_bar.grid(row=2,column=4,sticky = "NSEW")
        self.__buttons.grid(row=3,column=1)
        self.__delete_canvas_button.grid(row=3,column=2)
        self.__radio_buttons.grid(row=0,column=0,rowspan=4,sticky="NSEW")
        
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=4)
        self.columnconfigure(2,weight=2)
        self.columnconfigure(3,weight=2)
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
        self.__on_element_release()
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
        
        
    def __goal_set(self,string):
        
        self.__T.config(state=NORMAL)
        self.__T.delete("1.0","end")
        self.__T.insert(END, string)
        self.__T.config(state=DISABLED)
        self.thread_finish()
    
    def __goal_notfound(self):
        
        self.__T.config(state=NORMAL)
        self.__T.delete("1.0","end")
        self.__T.insert(END,"Goal wasnot found")
        self.__T.config(state=DISABLED)
        self.thread_finish()

    

if __name__ == "__main__":
    
    root =  Tk()
    root.geometry("1000x720")
    root.title('AI Graph Search')
    can = MainCanvas(root,920,720)
    
    can.grid(row=0,column=0,sticky = "NSEW")
    
    root.columnconfigure(0,weight=1)
    root.rowconfigure(0,weight=1)

    root.mainloop()
