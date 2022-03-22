from tkinter import *
from tkinter.ttk import *
import os
from settings import mouse,Mouse_state

class Button_Bar(Frame) :
    
    def __init__(self,root,width=200,height=200):
        
        Frame.__init__(self, root,width=width,height=height)
        self.grid_propagate(0)
        self.root = root
        
        circle_button = Button_Bar.create_button(self,os.path.join(os.getcwd(),'GUI','images','circle_resized.png'),self.circle_event)
        
        line_button = Button_Bar.create_button(self,os.path.join(os.getcwd(),'GUI','images','line_resized.png'),self.line_event)

        inital_node_button = Button_Bar.create_button(self,os.path.join(os.getcwd(),'GUI','images','start_resized.png'),self.inital_node_event)

        goal_button =  Button_Bar.create_button(self,os.path.join(os.getcwd(),'GUI','images','goal_resized.png'),self.goal_event)

        circle_button.grid(column=0,row=0,padx=10, pady=10)
        line_button.grid(column=0,row=1,padx=10, pady=10)
        inital_node_button.grid(column=0,row=2,padx=10, pady=10)
        goal_button.grid(column=0,row=3,padx=10, pady=10)

    @staticmethod
    def create_button(parent,img_path,callback):
        img = PhotoImage(file=img_path)
        button = Button(parent, image=img, command=callback)
        button.image = img        
        return button

    def circle_event(self):

        if (mouse.get_state() == Mouse_state.circle):
            mouse.set_state(Mouse_state.normal)              
            self.root.config(cursor="arrow")
        else:
            mouse.set_state(Mouse_state.circle)   
            self.root.config(cursor="cross")
                    

    def line_event(self):
        
        if (mouse.get_state() == Mouse_state.line):
            mouse.set_state(Mouse_state.normal)
            self.root.config(cursor="arrow")
        else:
            mouse.set_state(Mouse_state.line)
            self.root.config(cursor="plus")
           

    def inital_node_event(self):

        if (mouse.get_state() == Mouse_state.initial_node):
            mouse.set_state(Mouse_state.normal)
            self.root.config(cursor="arrow")
        else:
            mouse.set_state(Mouse_state.initial_node)
            self.root.config(cursor="spider")

    def goal_event(self):

        if (mouse.get_state() == Mouse_state.goal_node):
            mouse.set_state(Mouse_state.normal)
            self.root.config(cursor="arrow")
        else:
            mouse.set_state(Mouse_state.goal_node)
            self.root.config(cursor="target")



if __name__ == "__main__":

    root =  Tk()

    # root.geometry("300x300") 

    control = Button_Bar(root,500,500)

    control.grid()

    root.mainloop()


