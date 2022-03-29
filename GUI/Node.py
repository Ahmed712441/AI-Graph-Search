from abc import abstractmethod
from settings import *

class Element:

        
    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def delete(self):
        pass
    
    @abstractmethod
    def select(self):
        pass

    @abstractmethod
    def deselect(self):
        pass

    @abstractmethod
    def bind_event(self,callback):
        pass


class Line(Element):

    def __init__(self,canvas,Node_out,Node_in,weight=1):
        
        self.__id = None
        self.__canvas = canvas
        self.Node_in = Node_in
        self.Node_out = Node_out
        self.weight = weight


    def add_label(self):

        x1,y1,x2,y2 = self.__canvas.coords(self.__id)
        x = (x1 + x2)//2
        y = (y1 + y2)//2
        self.__label_id = self.__canvas.create_text((x, y), text=self.weight)

    def get_id(self):
        return self.__id


    def create(self):
        Node_in_x , Node_in_y = self.Node_in.get_coor()
        Node_out_x , Node_out_y = self.Node_out.get_coor()

        dy = abs(Node_in_y - Node_out_y)
        dx = abs(Node_in_x - Node_out_x)
        if(dx > dy):
            if(Node_in_y < Node_out_y):
                self.__id = self.__canvas.create_line(Node_out_x,Node_out_y+RADUIS,Node_in_x,Node_in_y+RADUIS,arrow="last",fill=LINE_COLOR_NORMAL)
            else:
                self.__id = self.__canvas.create_line(Node_out_x,Node_out_y-RADUIS,Node_in_x,Node_in_y-RADUIS,arrow="last",fill=LINE_COLOR_NORMAL)
        else:
            if(Node_in_x < Node_out_x):
                self.__id = self.__canvas.create_line(Node_out_x+RADUIS,Node_out_y,Node_in_x+RADUIS,Node_in_y,arrow="last",fill=LINE_COLOR_NORMAL)
            else:
                self.__id = self.__canvas.create_line(Node_out_x-RADUIS,Node_out_y,Node_in_x-RADUIS,Node_in_y,arrow="last",fill=LINE_COLOR_NORMAL)
            
        self.add_label()
        self.__canvas.lower(self.__id)

        return self

    def delete(self):
        
        self.Node_in.lines_in.remove(self)
        self.Node_out.lines_out.remove(self)
        self.Node_out.adj.remove(self.Node_in)
        self.__canvas.delete(self.__id)
        self.__canvas.delete(self.__label_id)

    def select(self):

        self.__canvas.itemconfig(self.__id, fill=LINE_COLOR_SELECTED)

    def deselect(self):

        self.__canvas.itemconfig(self.__id, fill=LINE_COLOR_NORMAL)
    
    def bind_event(self,callback,binded_event='<Button-1>'):
        
        self.__canvas.tag_bind(self.__label_id,binded_event,lambda event, arg=self.__id: callback(event, arg))
        self.__canvas.tag_bind(self.__id, binded_event, lambda event, arg=self.__id: callback(event, arg))

    def __str__(self):

        return "line id: "+str(self.__id) + " connecting:  "+str(self.Node_out) +" with "+str(self.Node_in) 


class Node(Element):

    def __init__(self,canvas,x,y,label,goal=False):

        self.adj = [] # carries adjancent nodes
        self.lines_out = [] # has all out lines 
        self.lines_in = [] # has all in lines
        self.__goal = goal # is this node a goal or not 
        self.__canvas = canvas # canvas object helps in drawing on screen
        self.__x = x # x coordinate of its center
        self.__y = y # y coordinate of its center
        self.label = label # unique label used to identify each node used mainly in GUI 
        self.__initial = False # boolean value to define if this node is initial or not

    def set_initial(self):

        self.__initial = True
        self.__reset_color()

    def reset_initial(self):
        
        self.__initial = False
        self.__reset_color()

    def set_goal(self):

        self.__goal = True
        self.__reset_color()

    def reset_goal(self):
        
        self.__goal = False
        self.__reset_color()

    def is_goal(self):
        
        return self.__goal

    def connect_node(self,node):

        if node in self.adj :
            raise DuplicateConnectionException()
            
        self.adj.append(node)
        l = Line(self.__canvas,self,node)
        l.create()       
        self.lines_out.append(l)
        node.lines_in.append(l)
        return l

    def get_coor(self):
        return self.__x , self.__y

    def __create_circle(self): 
        
        x0 = self.__x - RADUIS
        y0 = self.__y - RADUIS
        x1 = self.__x + RADUIS
        y1 = self.__y + RADUIS
        overlap = self.__canvas.find_overlapping(x0, y0, x1, y1)
        if len(overlap):
            raise OverlapException()
            
        return self.__canvas.create_oval(x0, y0, x1, y1,fill=CIRCLE_COLOR_NORMAL)


    def create(self):
        self.__id = self.__create_circle()
        self.__label_id = self.__canvas.create_text((self.__x, self.__y), text=self.label)
        return self.__id

    def get_id(self):
        return self.__id
    
    def delete(self):
        
        for line in self.lines_in + self.lines_out:
            line.delete()
        
        self.__canvas.delete(self.__id)
        self.__canvas.delete(self.__label_id)

    def select(self):

        self.__canvas.itemconfig(self.__id, fill=CIRCLE_COLOR_SELECTED)

    def __reset_color(self):
        
        if self.__goal and self.__initial:
            self.__canvas.itemconfig(self.__id, fill=GOAL_INITIAL_COLOR)
        elif self.__initial:
            self.__canvas.itemconfig(self.__id, fill=INITIAL_NODE_COLOR)
        elif self.__goal:
            self.__canvas.itemconfig(self.__id, fill=GOAL_NODE_COLOR)
        else:
            self.__canvas.itemconfig(self.__id, fill=CIRCLE_COLOR_NORMAL)

    def deselect(self):
        
        self.__reset_color()
        

    def bind_event(self,callback,binded_event='<Button-1>'):
        self.__canvas.tag_bind(self.__id, binded_event, lambda event, arg=self.__id: callback(event, arg))
        self.__canvas.tag_bind(self.__label_id, binded_event, lambda event, arg=self.__id: callback(event, arg))

    def __str__(self):
    
        return str(self.__id)

class TreeNode:

    def __init__(self,treecanvas,node,level,parent,x,y):
        
        self.__treecanvas = treecanvas # canvas object helps to draw tree
        self.__node = node # node object helps in visualiziation and concurrency
        self.__level = level # level which the Node is drawn in
        self.__x = x     # to avoid overlapping between childrens of another nodes 
        self.__y = y  # to avoid overlapping between childrens of another nodes 
        self.parent = parent # parent Node null if it's th root
        self.children = [] # childrens of the node
    
    def __create_circle(self): 
        
        x0 = self.__x - RADUIS
        y0 = self.__y - RADUIS
        x1 = self.__x + RADUIS
        y1 = self.__y + RADUIS
        overlap = self.__canvas.find_overlapping(x0, y0, x1, y1)
        if len(overlap):
            raise OverlapException()
            
        return self.__canvas.create_oval(x0, y0, x1, y1,fill=CIRCLE_COLOR_NORMAL)        
        
    def create(self):

        self.__id = self.__create_circle()
        self.__label_id = self.__canvas.create_text((self.__x, self.__y), text=self.__node.label)
        return self.__id

    
