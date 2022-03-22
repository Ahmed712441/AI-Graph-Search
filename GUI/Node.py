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
        
        self.id = None
        self.canvas = canvas
        self.Node_in = Node_in
        self.Node_out = Node_out
        self.weight = weight


    def add_label(self):

        x1,y1,x2,y2 = self.canvas.coords(self.id)
        x = (x1 + x2)//2
        y = (y1 + y2)//2
        self.label_id = self.canvas.create_text((x, y), text=self.weight)
        

    def create(self):
        
        dy = abs(self.Node_in.y - self.Node_out.y)
        dx = abs(self.Node_in.x - self.Node_out.x)
        if(dx > dy):
            if(self.Node_in.y < self.Node_out.y):
                self.id = self.canvas.create_line(self.Node_out.x,self.Node_out.y+RADUIS,self.Node_in.x,self.Node_in.y+RADUIS,arrow="last",fill=LINE_COLOR_NORMAL)
            else:
                self.id = self.canvas.create_line(self.Node_out.x,self.Node_out.y-RADUIS,self.Node_in.x,self.Node_in.y-RADUIS,arrow="last",fill=LINE_COLOR_NORMAL)
        else:
            if(self.Node_in.x < self.Node_out.x):
                self.id = self.canvas.create_line(self.Node_out.x+RADUIS,self.Node_out.y,self.Node_in.x+RADUIS,self.Node_in.y,arrow="last",fill=LINE_COLOR_NORMAL)
            else:
                self.id = self.canvas.create_line(self.Node_out.x-RADUIS,self.Node_out.y,self.Node_in.x-RADUIS,self.Node_in.y,arrow="last",fill=LINE_COLOR_NORMAL)
            
        self.add_label()
        self.canvas.lower(self.id)

        return self

    def delete(self):
        
        self.Node_in.lines_in.remove(self)
        self.Node_out.lines_out.remove(self)
        self.Node_out.adj.remove(self.Node_in)
        self.canvas.delete(self.id)
        self.canvas.delete(self.label_id)

    def select(self):

        self.canvas.itemconfig(self.id, fill=LINE_COLOR_SELECTED)

    def deselect(self):

        self.canvas.itemconfig(self.id, fill=LINE_COLOR_NORMAL)
    
    def bind_event(self,callback,binded_event='<Button-1>'):
        
        self.canvas.tag_bind(self.label_id,binded_event,lambda event, arg=self.id: callback(event, arg))
        self.canvas.tag_bind(self.id, binded_event, lambda event, arg=self.id: callback(event, arg))

    def __str__(self):

        return "line id: "+str(self.id) + " connecting:  "+str(self.Node_out) +" with "+str(self.Node_in) 


class Node(Element):

    def __init__(self,canvas,x,y,label,goal=False):

        self.adj = [] # carries adjancent nodes
        self.lines_out = [] # has all out lines 
        self.lines_in = [] # has all in lines
        self.goal = goal # is this node a goal or not 
        self.canvas = canvas # canvas object helps in drawing on screen
        self.x = x # x coordinate of its center
        self.y = y # y coordinate of its center
        self.label = label # unique label used to identify each node used mainly in GUI 



    def connect_node(self,node):

        if node in self.adj :
            raise DuplicateConnectionException()
            
        self.adj.append(node)
        l = Line(self.canvas,self,node)
        l.create()       
        self.lines_out.append(l)
        node.lines_in.append(l)
        return l

    def __create_circle(self): #center coordinates, radius
        
        x0 = self.x - RADUIS
        y0 = self.y - RADUIS
        x1 = self.x + RADUIS
        y1 = self.y + RADUIS
        overlap = self.canvas.find_overlapping(x0, y0, x1, y1)
        if len(overlap):
            raise OverlapException()
            
        return self.canvas.create_oval(x0, y0, x1, y1,fill=CIRCLE_COLOR_NORMAL)


    def create(self):
        self.id = self.__create_circle()
        self.label_id = self.canvas.create_text((self.x, self.y), text=self.label)
        return self.id

    def change_node_color(self):
        
        self.canvas.itemconfig(self.id, fill="red")

    def delete(self):
        

        for line in self.lines_in + self.lines_out:
            line.delete()
        
        self.canvas.delete(self.id)
        self.canvas.delete(self.label_id)


    def select(self):

        self.canvas.itemconfig(self.id, fill=CIRCLE_COLOR_SELECTED)

    def deselect(self):

        self.canvas.itemconfig(self.id, fill=CIRCLE_COLOR_NORMAL)

    def bind_event(self,callback,binded_event='<Button-1>'):
        self.canvas.tag_bind(self.id, binded_event, lambda event, arg=self.id: callback(event, arg))
        self.canvas.tag_bind(self.label_id, binded_event, lambda event, arg=self.id: callback(event, arg))

    def __str__(self):
    
        return str(self.id)


    