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
    
    @abstractmethod
    def reset(self):
        pass

class InteractionInterface:
    
    def __init__(self,canvas):
        
        self.__canvas = canvas
        self.has_cross = False
        
    
    def set_id(self,id):
        self.__id = id

    def mark_active(self):
        self.__canvas.itemconfig(self.__id, fill=ACTIVE_NODE_COLOR)

    def mark_visited(self):
        self.__canvas.itemconfig(self.__id, fill=VISITED_NODE_COLOR)

    def mark_fringe(self):
        self.__canvas.itemconfig(self.__id, fill=FRINGE_NODE_COLOR)
    
    def __delete_cross(self):
        self.__canvas.delete(self.__cross_line1)
        self.__canvas.delete(self.__cross_line2)

    def mark_goal_path(self):
        if self.has_cross:
            self.__delete_cross()
        self.__canvas.itemconfig(self.__id, fill=GOAL_PATH_COLOR)
    
    def mark_already_visited(self):
        self.mark_fringe()
        if not self.has_cross:
            self.__draw_cross()
        
    def __draw_cross(self):
        
        self.has_cross = True
        x,y = self.get_coor()
        self.__cross_line1 = self.__canvas.create_line(x+CROSS_DISTANCE , y+CROSS_DISTANCE,x-CROSS_DISTANCE , y-CROSS_DISTANCE,fill=ALREADY_VISITED_COLOR)
        self.__cross_line2 = self.__canvas.create_line(x-CROSS_DISTANCE , y+CROSS_DISTANCE,x+CROSS_DISTANCE , y-CROSS_DISTANCE,fill=ALREADY_VISITED_COLOR)
    
    def move_cross(self):
        x,y = self.get_coor()
        self.__canvas.coords(self.__cross_line1,x+CROSS_DISTANCE , y+CROSS_DISTANCE,x-CROSS_DISTANCE , y-CROSS_DISTANCE)
        self.__canvas.coords(self.__cross_line2,x-CROSS_DISTANCE , y+CROSS_DISTANCE,x+CROSS_DISTANCE , y-CROSS_DISTANCE)
