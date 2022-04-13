from tkinter import *
from tkinter import messagebox
from Node import Node 
from Buttons import Button_Bar
from settings import CANVAS_BACKGROUND_COLOR
from utils import mouse,Mouse_state


class DrawingCanvas(Frame):

    def __init__(self,root,width=400,height=400,canvas_width=2000,canvas_height=1300,event_root=None,onselect=None,onrelease=None):
        '''
        constructor
        '''
        self.root = root
        Frame.__init__(self, root) 
        self.count_nodes = 0 # this variable used to count nodes helpful in labeling nodes
        self.hor_scrollbar = Scrollbar(self, orient=HORIZONTAL)
        self.ver_scrollbar = Scrollbar(self, orient=VERTICAL)
        
        self.canvas = Canvas(self,background=CANVAS_BACKGROUND_COLOR,scrollregion=(0, 0, canvas_width, canvas_height),yscrollcommand=self.ver_scrollbar.set,xscrollcommand=self.hor_scrollbar.set) # canvas object
        self.hor_scrollbar['command'] = self.canvas.xview
        self.ver_scrollbar['command'] = self.canvas.yview
         
        self.connection_node = None # node which carry the id of previously selected node needed only in line case as line needs to connects two nodes so this is considered as the first node  
        self.objects = dict() # hash-map used for mapping objects_id (Lines and Nodes) on canvas to objects (Line or Node) 
        self.selected = None # carry the id of selected node to be edited , deleted
        self.initial_node = None # carry initial node
        
        self.canvas.grid(row=0,column=0,sticky=(N,W,E,S)) # places the canvas in row : 0 , column :0 in the frame
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        self.hor_scrollbar.grid(column=0, row=1, sticky=(W,E))
        self.ver_scrollbar.grid(column=1, row=0, sticky=(N,S))
        self.__on_select = onselect
        self.__on_release = onrelease
        mouse.set_callback(self.undo_selection) # add callback function when mouse changes its state (event)
        self.canvas.bind("<ButtonPress-1>", self.mouse_clicked) # add callback function on click event for canvas
        event_root =  event_root if event_root else root
        event_root.bind("<KeyPress>", self.key_pressed) # add callback function on keyboard press event for the whole window
        
    def key_pressed(self,event):
        
        '''
        function called when any keyboard key is called to check for node deletion
        '''
        
        focused = self.root.focus_get().__str__()
        
        if (event.keycode == 46 or event.keycode == 8) and self.selected and not (focused == ".!maincanvas.!entry2" or focused == ".!maincanvas.!entry3"): # keycode == 46 (<Delete key>) keycode == 8 (<Backspace key>) checks for delete press and node selection at the same moment
            
            if  isinstance(self.selected,Node):
                for line in self.selected.lines_in + self.selected.lines_out:
                    del self.objects[str(line.get_id())]
            
            if self.selected == self.initial_node :
                self.initial_node = None

            self.selected.delete() # get the node from the map and deletes it
            del self.objects[str(self.selected.get_id())] 
            self.selected = None
            self.__on_release()


    def undo_selection(self):

        '''
        function called when mouse_state changes to reset the selections to its initial state (Nothing is selected)
        '''
        # note: if item is selected color = blue , not selected color = green 

        if self.connection_node :
            
            self.connection_node.deselect()
            self.connection_node = None
            
        
        if self.selected:

            self.__on_release()
            self.selected.deselect()
            self.selected = None


    def mouse_clicked(self,event):

        '''
        function for listening to mouse click event on canvas and if the mouse_state was circle try to place circles in clicked place
        '''

        if mouse.get_state() == Mouse_state.circle: # check for mouse state
            
            n = Node(self.canvas,self.canvas.canvasx(event.x),self.canvas.canvasy(event.y),str(self.count_nodes)) # initialize node
            try:
                id = n.create() # create node
                self.objects[str(id)] = n # add node to nodes hash-table
                n.bind_event(self.node_clicked) # add click event to node
                 
                self.count_nodes+=1 # increment number of nodes
            except Exception as e: 
                messagebox.showerror(title=e.title,message=e)
                del n
            

    def node_clicked(self,event,canvas_item_id):

        '''
        function for listening to mouse click event on node it has many cases :
        1st case: mouse state was line and self.connection_node is not null so its the second point so we should connect the two points
        2nd case: mouse state was line and self.connection_node is null so we assign it to self.connection_node and wait for second node in order to connect them
        3rd case: mouse state is normal (neither circle nor line are selected) and self.selected is None so no node is selected so we self.selected will be equal to clicked node
        4th case: mouse state is normal and self.selected is not None so the we will deselect old node and select the new one
        5th case: mouse state is normal and self.selected is equal to clicked node so we will deselect this node and makes self.selected = None 
        '''

        if mouse.get_state() == Mouse_state.line: # checking for mouse state
            # 2nd case
            if not self.connection_node : 
                
                self.connection_node = self.objects[str(canvas_item_id)]
                self.connection_node.select() 
                
            else :
                # 5th case
                if canvas_item_id == self.connection_node.get_id():
                    
                    self.connection_node.deselect()
                    
                    self.connection_node = None
                # 1st case
                else :
                    try :
                        
                        line = self.connection_node.connect_node(self.objects[str(canvas_item_id)])
                        line.bind_event(self.line_clicked)
                        self.objects[str(line.get_id())] =  line
                        
                        self.connection_node.deselect()
                        self.connection_node = None

                    except Exception as e: 
                        
                        messagebox.showerror(title=e.title,message=e)
                    

        elif mouse.get_state() == Mouse_state.normal:
            # 3rd case
            if not self.selected : 
                
                self.selected = self.objects[str(canvas_item_id)] 
                self.selected.select()
                self.__on_select()
                 
            # 5th case
            elif self.selected.get_id() == canvas_item_id:
                self.__on_release()
                self.selected.deselect()
                self.selected = None
            # 4th case
            else:
                self.__on_release()
                self.selected.deselect()
                self.selected = self.objects[str(canvas_item_id)]
                self.selected.select()
                self.__on_select()

        elif mouse.get_state() == Mouse_state.initial_node:
            selected_node = self.objects[str(canvas_item_id)]
            
            if not self.initial_node:
                self.initial_node = selected_node
                self.initial_node.set_initial()
            
            elif self.initial_node == selected_node:
                self.initial_node.reset_initial()
                self.initial_node = None

            else:
                self.initial_node.reset_initial()
                self.initial_node = selected_node
                self.initial_node.set_initial()

        elif mouse.get_state() == Mouse_state.goal_node:

            selected_node = self.objects[str(canvas_item_id)]
            
            if selected_node.is_goal():
                selected_node.reset_goal()
            else:
                selected_node.set_goal()

    def reset_selected(self):
        
        if not self.selected : return

        self.selected.deselect()
        self.selected = None

    def line_clicked(self,event,canvas_item_id):

        if mouse.get_state() == Mouse_state.normal:
            
            if not self.selected : 
                self.selected = self.objects[str(canvas_item_id)]
                self.selected.select()
                self.__on_select()

            elif self.selected.get_id() == canvas_item_id :
                self.__on_release()
                self.reset_selected()
            
            else:
                self.__on_release()
                self.reset_selected()
                self.selected = self.objects[str(canvas_item_id)]
                self.selected.select()
                self.__on_select()
                
    def reset(self):
        for _,element in self.objects.items():
            element.reset()

    def delete_all(self):

        self.count_nodes = 0 
        self.connection_node = None 
        del self.objects
        self.objects = dict()  
        self.selected = None
        self.initial_node = None
        self.canvas.delete("all")
        



if __name__=="__main__":


    root =  Tk()
    root.geometry("1000x720")
    b = Button_Bar(root)
    can = DrawingCanvas(root,920,720)

    can.grid(row=0,column=0,sticky="NSEW")
    b.grid(row=0,column=1,sticky="NSEW")
    root.rowconfigure(0,weight=1)
    root.columnconfigure(0,weight=1)

    root.mainloop()







