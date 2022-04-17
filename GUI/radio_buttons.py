from tkinter import *
from tkinter.ttk import *
from Algorithms.Search_Algorithms import *

class AlgorithmsRadioButtons(Frame):

    def __init__(self,root,submit_callback,canvas=None):
        
        Frame.__init__(self, root)
        self.__var = IntVar()
        self.__depth_limited_text = Entry(self)
        self.__algorithms_label = Label(self,text = "Search Algorithms :")
        self.__uninformed_label = Label(self,text = "uninformed Search Algorithms :")
        self.__informed_label = Label(self,text = "informed Search Algorithms :")
        self.__breadth = Radiobutton(self, text='breadth first search', variable=self.__var, value=1)
        self.__depth_first = Radiobutton(self, text='depth first search', variable=self.__var, value=2)
        self.__depth_limited = Radiobutton(self, text='depth limited search', variable=self.__var, value=3)
        self.__iterative_deepening = Radiobutton(self, text='iterative deepening search', variable=self.__var, value=4)
        self.__uniform = Radiobutton(self, text='uniform search', variable=self.__var, value=5)
        self.__A = Radiobutton(self, text='A* search', variable=self.__var, value=6)
        self.__greedy = Radiobutton(self, text='greedy best first search', variable=self.__var, value=7)
        self.__button = Button(self ,text="Start Search" , command=self.__start_search)
        self.__submit_callback =submit_callback
        self.__canvas = canvas
        self.__depth_limited_text.bind('<FocusIn>',lambda x : self.__canvas.undo_selection())
        self.__pack_on_screen()

    def __pack_on_screen(self):

        self.__algorithms_label.grid(row=0,column=0,sticky="W",padx=(0, 5),pady=(5,5))
        self.__uninformed_label.grid(row=1,column=0,sticky="W",padx=(0, 5),pady=(10,10))
        self.__breadth.grid(row=2,column=0,sticky="W",padx=(0, 5),pady=(5,5))
        self.__depth_first.grid(row=3,column=0,padx=(0, 5),pady=(5,5),sticky="W")
        self.__depth_limited.grid(row=4,column=0,padx=(0, 5),pady=(5,5),sticky="W")
        self.__iterative_deepening.grid(row=5,column=0,padx=(0, 5),pady=(5,5),sticky="W")
        self.__uniform.grid(row=6,column=0,padx=(0, 5),pady=(5,5),sticky="W")
        self.__informed_label.grid(row=7,column=0,padx=(0, 5),pady=(10,10),sticky="W")
        self.__A.grid(row=8,column=0,padx=(0, 5),pady=(5,5),sticky="W")
        self.__greedy.grid(row=9,column=0,padx=(0, 5),pady=(5,5),sticky="W")
        self.__button.grid(row=10,column=0,sticky = "NSEW",pady=(5,5))
        self.__depth_limited_text.grid(row=4,column=1)
        self.rowconfigure("all",weight=1)

    def __start_search(self):
        num = self.__var.get()
        if num == 1:
            self.__submit_callback(BreadthFirstSearch)
        elif num == 2:
            self.__submit_callback(DepthFirstSearch)
        elif num == 3:
            self.__submit_callback(DepthLimitedSearch,limit=int(self.__depth_limited_text.get()))
        elif num == 4:
            self.__submit_callback(IterativeDeepeningSearch,canvas=self.__canvas)
        elif num == 5:
            self.__submit_callback(UniformCostSearch)
        elif num == 6:
            self.__submit_callback(AStarSearch)
        elif num == 7:
            self.__submit_callback(GreedyBestFirstSearch)

    def disable(self):
        self.__button.config(state=DISABLED)
    
    def enable(self):
        self.__button.config(state=NORMAL)

if __name__ ==  "__main__":
    
    root = Tk()

    content = AlgorithmsRadioButtons(root)
    content.grid(column=0, row=0, sticky=(N, S, E, W))

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)


    root.mainloop()    

