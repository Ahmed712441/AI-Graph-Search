from tkinter import *
from tkinter.ttk import *
import os
from utils import mouse,Mouse_state

class Button_Bar(Frame) :
    
    def __init__(self,root,width=300,height=400):
        
        Frame.__init__(self, root,width=width,height=height)
        
        self.root = root
        
        self.__circle_button = Button_Bar.create_button(self,os.path.join(os.getcwd(),'GUI','images','circle_resized.png'),self.circle_event)
        
        self.__line_button = Button_Bar.create_button(self,os.path.join(os.getcwd(),'GUI','images','line_resized.png'),self.line_event)

        self.__inital_node_button = Button_Bar.create_button(self,os.path.join(os.getcwd(),'GUI','images','start_resized.png'),self.inital_node_event)

        self.__goal_button =  Button_Bar.create_button(self,os.path.join(os.getcwd(),'GUI','images','goal_resized.png'),self.goal_event)

        self.__circle_button.grid(column=0,row=0,padx=10, pady=10)
        self.__line_button.grid(column=0,row=1,padx=10, pady=10)
        self.__inital_node_button.grid(column=0,row=2,padx=10, pady=10)
        self.__goal_button.grid(column=0,row=3,padx=10, pady=10)

    @staticmethod
    def create_button(parent,img_path,callback):
        img = PhotoImage(file=img_path)
        button = Button(parent, image=img, command=callback)
        button.image = img        
        return button

    def circle_event(self):

        if (mouse.get_state() == Mouse_state.circle):
            mouse.set_state(Mouse_state.normal)              
        else:
            mouse.set_state(Mouse_state.circle)   
            
                    

    def line_event(self):
        
        if (mouse.get_state() == Mouse_state.line):
            mouse.set_state(Mouse_state.normal)
            
        else:
            mouse.set_state(Mouse_state.line)
            
           

    def inital_node_event(self):

        if (mouse.get_state() == Mouse_state.initial_node):
            mouse.set_state(Mouse_state.normal)
            
        else:
            mouse.set_state(Mouse_state.initial_node)
            
    def goal_event(self):

        if (mouse.get_state() == Mouse_state.goal_node):
            mouse.set_state(Mouse_state.normal)
            
        else:
            mouse.set_state(Mouse_state.goal_node)
            

    def disable(self):
        self.__circle_button.config(state=DISABLED)
        self.__line_button.config(state=DISABLED)
        self.__inital_node_button.config(state=DISABLED)
        self.__goal_button.config(state=DISABLED)
        mouse.set_state(Mouse_state.disabled)

    def enable(self):
        self.__circle_button.config(state=NORMAL)
        self.__line_button.config(state=NORMAL)
        self.__inital_node_button.config(state=NORMAL)
        self.__goal_button.config(state=NORMAL)
        mouse.set_state(Mouse_state.normal)
        



class InteractionButtons(Frame):

    def __init__(self,root,pause_callback,start_callback,terminate_callback,delete_callback,width=300,height=400):
        
        Frame.__init__(self, root,width=width,height=height)
        self.pause = Button_Bar.create_button(self,os.path.join(os.getcwd(),'GUI','images','pause_icon.png'),pause_callback)
        self.resume = Button_Bar.create_button(self,os.path.join(os.getcwd(),'GUI','images','resume_icon.png'),start_callback)
        self.terminate = Button_Bar.create_button(self,os.path.join(os.getcwd(),'GUI','images','terminate.png'),terminate_callback)
        self.delete = Button_Bar.create_button(self,os.path.join(os.getcwd(),'GUI','images','delete_icon.png'),delete_callback)
        self.pause.config(state=DISABLED)
        self.resume.config(state=DISABLED)
        self.terminate.config(state=DISABLED)
        self.delete.config(state=DISABLED)
        self.pack_on_screen()

    def pack_on_screen(self):
        self.resume.grid(row=0,column=0)
        self.pause.grid(row=0,column=1)
        self.terminate.grid(row=0,column=2)
        self.delete.grid(row=0,column=3)
        

class DrawingCanvasButtons(Frame):

    def __init__(self,root,delete_callback,save_callback,upload_callback,width=300,height=400):
        
        Frame.__init__(self, root,width=width,height=height)
        self.__delete = Button_Bar.create_button(self,os.path.join(os.getcwd(),'GUI','images','delete_icon.png'),delete_callback)
        self.__save = Button_Bar.create_button(self,os.path.join(os.getcwd(),'GUI','images','save_icon.png'),save_callback)
        self.__load = Button_Bar.create_button(self,os.path.join(os.getcwd(),'GUI','images','upload_icon.png'),upload_callback)
        self.pack_on_screen()

    def pack_on_screen(self):
        self.__save.grid(row=0,column=0)
        self.__load.grid(row=0,column=1)
        self.__delete.grid(row=0,column=2)
        




if __name__ == "__main__":

    root =  Tk()

    # root.geometry("300x300") 

    # control = Button_Bar(root,50,280)

    # control.grid(sticky = "NSEW")

    # control = InteractionButtons(root,None,None,None,None)
    # control.grid(sticky = "NSEW")
    # DrawingCanvasButtons(root)
    control = DrawingCanvasButtons(root,None,None,None,None)
    control.grid(sticky = "NSEW")
    root.mainloop()


