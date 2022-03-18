from tkinter import *
from tkinter import messagebox
from Node import Node
from Buttons import Button_Bar,Mouse_state
from Buttons import mouse


class DrawingCanvas(Frame):

    def __init__(self,root,width=200,height=200):
        
        '''
        constructor
        '''
        Frame.__init__(self, root,width=width,height=height) 
        self.count_nodes = 0 # this variable used to count nodes helpful in labeling nodes
        self.canvas = Canvas(self,background="grey") # canvas object
        self.control_bar = Button_Bar(self) # side bar which contains (circle,line) buttons and forms for editing nodes 
        self.connection_node = None # node which carry the id of previously selected node needed only in line case as line needs to connects two nodes so this is considered as the first node  
        self.nodes = dict() # hash-map used for mapping node_id on canvas to Node object id
        self.selected_node = None # carry the id of selected node to be edited , deleted
        self.grid_propagate(0) # used to assures that frame will take its height and width even its children are smaller
        self.canvas.grid(row=0,column=0)  # places the canvas in row : 0 , column :0 in the frame
        self.control_bar.grid(column=1,row=0) # places the control_bar in row : 0 , column :1 in the frame
        mouse.set_callback(self.undo_selection) # add callback function when mouse changes its state (event)
        self.canvas.bind("<ButtonPress-1>", self.mouse_clicked) # add callback function on click event for canvas
        root.bind("<KeyPress>", self.delete_node) # add callback function on keyboard press event for the whole window
        

    def delete_node(self,event):
        
        '''
        function called when any keyboard key is called to check for node deletion
        '''
        
        if event.keycode == 46 and self.selected_node : # keycode == 46 (<Delete key>) checks for delete press and node selection at the same moment

            self.nodes[str(self.selected_node)].delete_node() # get the node from the map and deletes it
            del self.nodes[str(self.selected_node)] 
            self.selected_node = None 


    def undo_selection(self):

        '''
        function called when mouse_state changes to reset the selections to its initial state (Nothing is selected)
        '''
        # note: if item is selected color = blue , not selected color = green 


        if self.connection_node :
            self.canvas.itemconfig(self.connection_node, fill="#0f0") # reseting item color to normal color (green)
            self.connection_node = None
        
        if self.selected_node:
            self.canvas.itemconfig(self.selected_node, fill="#0f0") # reseting item color to normal color (green)
            self.selected_node = None

    def mouse_clicked(self,event):

        '''
        function for listening to mouse click event on canvas and if the mouse_state was circle try to place circles in clicked place
        '''

        if mouse.get_state() == Mouse_state.circle: # check for mouse state
            
            n = Node(self.canvas,event.x,event.y,str(self.count_nodes)) # initialize node
            try:
                id = n.create_node() # create node
                self.nodes[str(id)] = n # add node to nodes hash-table
                self.canvas.tag_bind(id, '<Button-1>', self.item_clicked) # add click event to node
                self.count_nodes+=1 # increment number of nodes
            except : # catch exception raised by n.create_node() if it overlaps with another node on the canvas
                messagebox.showerror(title="Overlaping Error",message="Can't place the node as it overlaps with another node") # show messagebox illustrates to the user the Overlaping error
                del n
            

    def item_clicked(self,event):

        '''
        function for listening to mouse click event on node it has many cases :
        1st case: mouse state was line and self.connection_node is not null so its the second point so we should connect the two points
        2nd case: mouse state was line and self.connection_node is null so we assign it to self.connection_node and wait for second node in order to connect them
        3rd case: mouse state is normal (neither circle nor line are selected) and self.selected_node is None so no node is selected so we self.selected_node will be equal to clicked node
        4th case: mouse state is normal and self.selected_node is not None so the we will deselect old node and select the new one
        5th case: mouse state is normal and self.selected_node is equal to clicked node so we will deselect this node and makes self.selected_node = None 
        '''

        canvas_item_id = event.widget.find_withtag('current')[0] # getting the id of clicked item

        if mouse.get_state() == Mouse_state.line: # checking for mouse state
            # 2nd case
            if not self.connection_node : 
                
                self.connection_node = canvas_item_id
                self.canvas.itemconfig(canvas_item_id, fill="blue") # changing item color to be noticed by the user that he selected an item

            else :
                # 5th case
                if canvas_item_id == self.connection_node:
                    self.canvas.itemconfig(self.connection_node, fill="#0f0")
                    self.connection_node = None
                # 1st case
                else :
                    self.nodes[str(self.connection_node)].connect_node(self.nodes[str(canvas_item_id)])
                    self.canvas.itemconfig(self.connection_node, fill="#0f0")
                    self.connection_node = None

        elif mouse.get_state() == Mouse_state.normal:
            # 3rd case
            if not self.selected_node : 
                
                self.selected_node = canvas_item_id
                self.canvas.itemconfig(canvas_item_id, fill="blue") 
            # 5th case
            elif self.selected_node == canvas_item_id:

                self.canvas.itemconfig(self.selected_node, fill="#0f0")
                self.selected_node = None
            # 4th case
            else:
                self.canvas.itemconfig(self.selected_node, fill="#0f0")
                self.selected_node = canvas_item_id
                self.canvas.itemconfig(self.selected_node, fill="blue")






if __name__=="__main__":


    root =  Tk()
    root.geometry("500x500")

    can = DrawingCanvas(root,500,500)

    can.grid()


    root.mainloop()







