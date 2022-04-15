from abc import abstractmethod
from settings import *
from Interfaces import Element,InteractionInterface
from utils import OverlapException,DuplicateConnectionException

class Line(Element):

    def __init__(self,canvas,Node_out,Node_in,weight=1):
        
        self.__id = None
        self.__canvas = canvas
        self.Node_in = Node_in
        self.Node_out = Node_out
        self.__weight = weight

    def get_save_data(self):

        return  str(self.__weight) + '\t' + str(self.Node_out.get_id()) + '\t' + str(self.Node_in.get_id())  +  '\n'

    def get_weight(self):
        return self.__weight
    
    def set_weight(self,new_weight:int):
      
        if new_weight != self.__weight:
            self.__weight = new_weight
            self.__canvas.itemconfig(self.__label_id, text=str(new_weight))


    def __add_label(self):

        x1,y1,x2,y2 = self.__canvas.coords(self.__id)
        x = (x1 + x2)//2
        y = (y1 + y2)//2
        self.__label_id = self.__canvas.create_text((x, y), text=self.__weight)

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
            
        self.__add_label()
        self.__canvas.lower(self.__id)

        return self

    def set_brother(self,line_id,treecanvas):
        self.__tree_line = line_id
        self.__tree_canvas = treecanvas

    def reset(self):
        self.__tree_line = None
        self.__tree_canvas = None
        self.deselect()
        

    def set_active(self):
        
        self.select()
        self.__tree_canvas.itemconfig(self.__tree_line, fill=ACTIVE_LINE_COLOR)
    
    def set_goal_path(self):

        self.select()
        self.__tree_canvas.itemconfig(self.__tree_line, fill=GOAL_PATH_LINE_COLOR)
    
    def reset_line(self):
        
        self.deselect()
        self.__tree_canvas.itemconfig(self.__tree_line, fill=LINE_COLOR_NORMAL)
    

    def delete(self):
        
        self.Node_in.lines_in.remove(self)
        self.Node_out.lines_out.remove(self)
        self.Node_out.adj.remove(self.Node_in)
        self.__canvas.delete(self.__id)
        self.__canvas.delete(self.__label_id)



    def select(self):

        self.__canvas.itemconfig(self.__id, fill=LINE_COLOR_SELECTED)
        self.__canvas.itemconfig(self.__label_id,fill=GOAL_PATH_LINE_LABEL_COLOR)

    def deselect(self):

        self.__canvas.itemconfig(self.__id, fill=LINE_COLOR_NORMAL)
        self.__canvas.itemconfig(self.__label_id,fill=LINE_LABEL_COLOR)
    
    def bind_event(self,callback,binded_event='<Button-1>'):
        
        self.__canvas.tag_bind(self.__label_id,binded_event,lambda event, arg=self.__id: callback(event, arg))
        self.__canvas.tag_bind(self.__id, binded_event, lambda event, arg=self.__id: callback(event, arg))

    def __str__(self):

        return "line id: "+str(self.__id) + " connecting:  "+str(self.Node_out) +" with "+str(self.Node_in) 


class Node(Element,InteractionInterface):

    def __init__(self,canvas,x,y,label,heurastic=0,goal=False,initial=False,expanded_level=1000000):
        super(Node,self).__init__(canvas)
        self.adj = [] # carries adjancent nodes
        self.lines_out = [] # has all out lines 
        self.lines_in = [] # has all in lines
        self.__goal = goal # is this node a goal or not 
        self.__canvas = canvas # canvas object helps in drawing on screen
        self.__x = x # x coordinate of its center
        self.__y = y # y coordinate of its center
        self.__label = label # unique label used to identify each node used mainly in GUI 
        self.__initial = initial # boolean value to define if this node is initial or not
        self.__heurastic = heurastic
        self.visited = False
        self.__expanded_level = expanded_level
    
    def get_save_data(self):
        initial = '1' if self.__initial else '0'
        goal = '1' if self.__goal else '0'
        return str(self.__id) + '\t' + str(self.__label) + '\t' + str(self.__x) + '\t' + str(self.__y) + '\t' + str(self.__heurastic) + '\t' + initial + '\t' + goal +'\n'

    def set_heurastic(self,new_heurastic:int):
        
        if new_heurastic != self.__heurastic:
            self.__heurastic = new_heurastic
            self.__canvas.itemconfig(self.__heurastic_id, text=str(self.__heurastic))
    
    def get_heurastic(self):
        return self.__heurastic

    def get_label(self):
        return self.__label

    def set_label(self,new_label):
        if new_label != self.__label:
            self.__label = new_label
            self.__canvas.itemconfig(self.__label_id, text=str(new_label))


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

    def connect_node(self,node,weight=1):

        if node in self.adj :
            raise DuplicateConnectionException()
            
        self.adj.append(node)
        l = Line(self.__canvas,self,node,weight)
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
        self.__label_id = self.__canvas.create_text((self.__x, self.__y), text=self.__label)
        self.__heurastic_id = self.__canvas.create_text((self.__x-RADUIS, self.__y-RADUIS), text=self.__heurastic,fill=VALUE_COLOR)
        super(Node,self).set_id(self.__id)
        return self.__id

    def get_id(self):
        return self.__id
    
    def delete(self):
        
        for line in self.lines_in + self.lines_out:
            line.delete()
        
        self.__canvas.delete(self.__id)
        self.__canvas.delete(self.__label_id)
        self.__canvas.delete(self.__heurastic_id)

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
    
        return "Node("+ str(self.__label)+")"

    def mark_visited(self):
        super().mark_visited()
        self.visited = True
    
    def reset(self):
        super().reset_cross()
        self.__reset_color()
        self.visited = False

    def set_expanded_level(self,level):
        self.__expanded_level = level if level < self.__expanded_level else self.__expanded_level

    def get_expanded_level(self):
        return self.__expanded_level
        
    def is_initial(self):
        return self.__initial

    def load(self,string:str):
        # 1	0	455.0	60.0	0	1	0
        # self.__id  self.__label  self.__x  self.__y self.__heurastic initial goal
        
        attr = string.split('\t')
        self.__label = attr[1]
        self.__x = float(attr[2])
        self.__y = float(attr[3])
        self.__heurastic = int(attr[4])
        self.__initial = (attr[5] == '1') 
        self.__goal = (attr[6] =='1')
        self.create()
        self.__reset_color()