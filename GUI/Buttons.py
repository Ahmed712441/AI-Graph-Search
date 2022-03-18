from tkinter import *
from tkinter.ttk import *
import os
# import enum



class Mouse_state:
   
    normal  = 1           # neither circle nor line is clicked 
    circle = 2           # circle is clicked
    line   = 3           # line is clicked

    def __init__(self):
        self.__state = Mouse_state.normal
        self.callback = None    

    def set_callback(self,callback):
        self.callback = callback


    def set_state(self,new_state):
        
        if self.callback :
            self.callback()
            self.__state = new_state
        else:
            self.__state = new_state

    def get_state(self):
        
        return self.__state
    

mouse = Mouse_state()

class Button_Bar(Frame) :
    
    def __init__(self,root,width=200,height=200):
        
        Frame.__init__(self, root,width=width,height=height)
        self.grid_propagate(0)
        # self.mouse = Mouse_state.normal # describes mouse state
        self.root = root
        circle_img = PhotoImage(file=os.path.join(os.getcwd(),'GUI','images','circle_resized.png'))
        line_img = PhotoImage(file=os.path.join(os.getcwd(),'GUI','images','line_resized.png'))
        circle_button = Button(self,image=circle_img ,command=self.circle_event)
        circle_button.image = circle_img
        line_button = Button(self, image=line_img, command=self.line_event)
        line_button.image = line_img
        circle_button.grid(column=0,row=0,padx=10, pady=10)
        line_button.grid(column=0,row=1,padx=10, pady=10)


    def circle_event(self):
        
        if mouse.get_state() == Mouse_state.normal  or mouse.get_state() == Mouse_state.line :
            mouse.set_state(Mouse_state.circle)   
            self.root.config(cursor="cross")
        elif mouse.get_state() == Mouse_state.circle:
            mouse.set_state(Mouse_state.normal)              
            self.root.config(cursor="arrow")

    def line_event(self):
        
        if mouse.get_state() == Mouse_state.normal or mouse.get_state() == Mouse_state.circle :
            mouse.set_state(Mouse_state.line)
            self.root.config(cursor="plus")
        elif mouse.get_state() == Mouse_state.line or mouse.get_state() == Mouse_state.line_1 :
            mouse.set_state(Mouse_state.normal)
            self.root.config(cursor="arrow")






if __name__ == "__main__":

    root =  Tk()

    # root.geometry("500x500") 

    control = Button_Bar(root)

    control.grid()

    root.mainloop()


