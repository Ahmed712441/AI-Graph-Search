import sys
from settings import * 

sys.path.append(BASE_DIR)

from tkinter import *
from settings import * 
from tkinter.ttk import *
from treecanvas import TreeCanvas
from canvas import DrawingCanvas
from Buttons import *
from treenode import TreeNode
from radio_buttons import AlgorithmsRadioButtons
from Node import Line,Node
from utils import mouse
from tkinter.filedialog import *

class MainCanvas(Frame):

    def __init__(self,root,width=200,height=200):
        self.width = width
        Frame.__init__(self, root,width=width,height=height) 
        mouse.set_root(self)
        self.__drawing_canvas = DrawingCanvas(self,width//2,height-120,event_root = root,onselect=self.__on_element_selection,onrelease=self.__on_element_release)
        self.__tree_canvas = TreeCanvas(self,width//2,height-120)
        self.__control_bar = Button_Bar(self)
        self.__buttons = InteractionButtons(self,self.pause_callback,self.resume_callback,self.terminate_callback,self.delete_all)
        self.__goal_label = Label(self,text = "Goal path :")
        self.__T = Entry(self)
        self.__T.insert(END, "Goal path will appear here")
        self.__T.config(state=DISABLED)
        self.__H_label = Label(self,text = "Weight or Heurastic : ")
        self.__H_text = Entry(self)
        self.__H_text.insert(END, "weight (Line) , Heurastic(Node)")
        self.__H_text.config(state=DISABLED)
        self.__Name_label = Label(self,text = "Change Node Name :")
        self.__Name_text = Entry(self)
        self.__Name_text.insert(END, "Change node name")
        self.__Name_text.config(state=DISABLED)
        self.__Name_text.bind('<Return>',lambda x: self.__change_node())
        self.__H_text.bind('<Return>',lambda x: self.__change_node())
        self.__submit_changes = Button(self ,text="Submit Changes" , command=self.__change_node)
        self.__submit_changes.config(state=DISABLED)
        self.__current_thread = None   
        self.__radio_buttons = AlgorithmsRadioButtons(self,self.__submit_callback,self.__drawing_canvas)
        self.__drawing_canvas_buttons = DrawingCanvasButtons(self,self.__drawing_canvas.delete_all,self.__on_save,self.__on_upload)
        self.__pack_on_screen()
    
    def __on_save(self):
        file_path = asksaveasfilename(initialfile='Untitled.gtxt',
                                        defaultextension=".gtxt",
                                        filetypes=[
                                            ("Graph Documents","*.gtxt")])
        self.__drawing_canvas.save(file_path)
    
    def __on_upload(self):
        file_path = askopenfilename(defaultextension=".gtxt",
                                      filetypes=[
                                        ("Graph Documents","*.gtxt")])
        self.__drawing_canvas.load(file_path)

    def __on_element_selection(self):
        self.focus()
        if isinstance(self.__drawing_canvas.selected , Line):
            self.__H_text.config(state=NORMAL)
            self.__submit_changes.config(state=NORMAL)
            self.__H_text.delete(0, 'end')
            self.__H_text.insert(END, str(self.__drawing_canvas.selected.get_weight()))
        if isinstance(self.__drawing_canvas.selected , Node):
            self.__Name_text.config(state=NORMAL)
            self.__H_text.config(state=NORMAL)
            self.__submit_changes.config(state=NORMAL)
            self.__H_text.delete(0, 'end')
            self.__Name_text.delete(0, 'end')
            self.__H_text.insert(END, str(self.__drawing_canvas.selected.get_heurastic()))
            self.__Name_text.insert(END, str(self.__drawing_canvas.selected.get_label()))
            
    
    def __on_element_release(self):
        
        self.__H_text.delete(0, 'end')
        self.__Name_text.delete(0, 'end')
        self.__Name_text.insert(END, "Change node name")
        self.__H_text.insert(END, "weight (Line) , Heurastic(Node)")
        self.__H_text.config(state=DISABLED)
        self.__submit_changes.config(state=DISABLED)
        self.__Name_text.config(state=DISABLED)
        

    def __change_node(self):
        if isinstance(self.__drawing_canvas.selected , Line):
            self.__drawing_canvas.selected.set_weight(int(self.__H_text.get()))
        elif isinstance(self.__drawing_canvas.selected , Node):
            self.__drawing_canvas.selected.set_heurastic(int(self.__H_text.get()))
            self.__drawing_canvas.selected.set_label(self.__Name_text.get())
    
    def __submit_callback(self,thread_class,**kwargs):

        if self.__drawing_canvas.initial_node and not self.__current_thread:
            self.__tree_canvas.canvas.delete("all")
            initial_node = TreeNode(self.__tree_canvas.canvas,0,None,0,self.__tree_canvas.canvas.winfo_width(),self.__drawing_canvas.initial_node)
            self.__current_thread = thread_class(initial_node,self.__goal_set,self.__goal_notfound,**kwargs)
            self.__current_thread.start()
            self.__buttons.delete.config(state=DISABLED)
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
        self.__drawing_canvas_buttons.grid(row=3,column=2,columnspan=2)
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
        self.__T.delete(0,"end")
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
        self.__T.delete(0,"end")
        self.__T.insert(END, string)
        self.__T.config(state=DISABLED)
        self.thread_finish()
    
    def __goal_notfound(self):
        
        self.__T.config(state=NORMAL)
        self.__T.delete(0,"end")
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
