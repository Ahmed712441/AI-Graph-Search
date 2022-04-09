from tkinter import *
from turtle import right
from settings import *

'''
testing file for tree drawing algorithm
'''

class TreeNodeTest:

    def __init__(self,treecanvas,level,parent,left,right):
        self.__canvas = treecanvas
        self.__level = level
        self.__x = (left+right)/2
        self.__y = level*TREE_VER_DISTANCE + 40
        self.__parent = parent
        self.__children = []
        self.__left = left
        self.__right = right
        self.__max_width = right - left  
        self.__max_nodes = self.__max_width // TREE_NODE_RADUIS
        self.__weight = 1

    def weight(self):
        return self.__weight

    def add_weight(self):
        self.__weight+=1

    def has_children(self):
        return len(self.__children) > 0

    def draw(self):
        self.__id = self.__create_circle()
        self.bind_event()
    
    def delete(self):
        self.__canvas.delete(self.__id)

    def move_to(self,new_x):
        
        diff = new_x - self.__x 
        self.__x = new_x
        self.__canvas.move(self.__id,diff,0)
    
    def change_margins(self,left,right):
       
        self.__left = left
        self.__right = right
        self.__max_width = right - left
        self.__max_nodes = self.__max_width // TREE_NODE_RADUIS
        self.move_to((right + left)/2)
        if len(self.__children) > 0:
            self.reset_children(0)

    def __create_add_node(self,left,right):

        node = TreeNodeTest(self.__canvas,self.__level+1,self,left,right)
        node.draw()
        self.__children.append(node)

    def children_total_weight(self):
        sum = 0
        for child in self.__children:
            sum += child.weight()
        return sum

    def __reset_margin(self,add_node:int):
        
        nodes = self.children_total_weight()
        node_width = self.__max_width / (nodes+add_node)     
        left_bounding = self.__left
        for child in self.__children:
            right_bounding = left_bounding+node_width*child.weight()
            child.change_margins(left_bounding,right_bounding)
            left_bounding = right_bounding

        return right_bounding , node_width

    def reset_children(self,add_node:int):
        
        left_bounding,node_width = self.__reset_margin(add_node)
 
        if(add_node > 0):
            right_bounding = left_bounding+node_width
            self.__create_add_node(left_bounding,right_bounding)
            self.add_weight()
            if self.__parent:
                self.__parent.add_weight()
        

    def reset_parent(self):
        if self.__parent:
            self.__parent.reset_children(0)
            self.__parent.reset_parent()

    def add_child(self):
        num_of_nodes = len(self.__children)
        if num_of_nodes == 0:
            self.__create_add_node(self.__left,self.__right)
        else:
            self.reset_children(1)
            self.reset_parent()

    def __create_circle(self): 
        
        x0 = self.__x - TREE_NODE_RADUIS
        y0 = self.__y - TREE_NODE_RADUIS
        x1 = self.__x + TREE_NODE_RADUIS
        y1 = self.__y + TREE_NODE_RADUIS
         
        return self.__canvas.create_oval(x0, y0, x1, y1,fill=CIRCLE_COLOR_NORMAL)

    def bind_event(self):
        self.__canvas.tag_bind(self.__id,'<Button-1>',lambda x : self.add_child())


class TreeCanvasTest(Frame):

    def __init__(self,root,width=200,height=200,canvas_width=1000,canvas_height=1000):
        
        Frame.__init__(self, root,width=width,height=height) 
        self.count_nodes = 0 # this variable used to count nodes helpful in labeling nodes
        self.hor_scrollbar = Scrollbar(self, orient=HORIZONTAL)
        self.ver_scrollbar = Scrollbar(self, orient=VERTICAL)
        self.canvas = Canvas(self,height=height-100,width=width-100,background=CANVAS_BACKGROUND_COLOR,scrollregion=(0, 0, canvas_width, canvas_height),yscrollcommand=self.ver_scrollbar.set,xscrollcommand=self.hor_scrollbar.set) # canvas object
        self.hor_scrollbar['command'] = self.canvas.xview
        self.ver_scrollbar['command'] = self.canvas.yview
        self.grid_propagate(0) # used to assures that frame will take its height and width even its children are smaller
        self.canvas.grid(row=0,column=0,sticky=(N,W,E,S))  # places the canvas in row : 0 , column :0 in the frame
        self.hor_scrollbar.grid(column=0, row=1, sticky=(W,E))
        self.ver_scrollbar.grid(column=1, row=0, sticky=(N,S))
        # self.canvas.bind('<Button-1>',lambda event : print(event.x,event.y))
    
    def draw_node(self):
        pass


if __name__=="__main__":


    root =  Tk()
    root.geometry("600x600")

    can = TreeCanvasTest(root,500,500)
    n = TreeNodeTest(can.canvas ,0,None,0,400)
    n.draw()
    can.grid()


    root.mainloop()