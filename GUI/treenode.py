from settings import *
from abc import abstractmethod


class TreeNodeDrawing:

    def __init__(self,treecanvas,level,parent,left,right,sub_class,Line=None):
        self.__canvas = treecanvas
        self.__level = level
        self.__x = (left+right)/2
        self.__y = level*TREE_VER_DISTANCE + 40
        self.__parent = parent
        self.__children = []
        self.__left = left
        self.__right = right
        self.__max_width = right - left  
        self.__weight = 1
        self.__parent_line = Line
        self.__sub_class = sub_class
        self.draw()

    def getchildren(self):
        return self.__children

    def set_parent_line(self,Line):

        self.__parent_line = Line
    
    def weight(self):
        return self.__weight

    def add_weight(self,added=1):
        self.__weight+=added
        if self.__parent:
            self.__parent.add_weight(added)

    def has_children(self):
        return len(self.__children) > 0

    def draw(self):
        self.__id = self.__create_circle()
       
    
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
        self.move_to((right + left)/2)
        self.move_line()
        if len(self.__children) > 0 :
            self.reset_children(0)

    def move_line(self):
        x,y = self.__parent.get_coor()
        self.__canvas.coords(self.__parent_line,x,y+TREE_NODE_RADUIS,self.__x,self.__y-TREE_NODE_RADUIS)
    
    def get_coor(self):
        return self.__x , self.__y


    def create_line(self,child_coor):
        return self.__canvas.create_line(self.__x , self.__y+TREE_NODE_RADUIS,child_coor[0],child_coor[1]-TREE_NODE_RADUIS,arrow="last",fill=LINE_COLOR_NORMAL)

    def __create_add_node(self,left,right,node):

        
        node = self.__sub_class(self.__canvas,self.__level+1,self,left,right,node)
        line = self.create_line(node.get_coor())
        node.set_parent_line(line)
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

    def reset_children(self,add_node:int,node=None):
        
        left_bounding,node_width = self.__reset_margin(add_node)
 
        if(add_node > 0):
            right_bounding = left_bounding+node_width
            self.__create_add_node(left_bounding,right_bounding,node)
            
            
    def reset_parent(self):
        if self.__parent:
            self.__parent.reset_parent()
        else:
            self.reset_children(0)
            

    def add_children(self,nodes):
        for node in nodes:
            self.__add_child(node)

    def __add_child(self,node):
        
        num_of_nodes = len(self.__children)
        if num_of_nodes == 0:
            self.__create_add_node(self.__left,self.__right,node)
        else:
            self.add_weight()
            self.reset_parent()
            self.reset_children(1,node)
            

    def __create_circle(self): 
        
        x0 = self.__x - TREE_NODE_RADUIS
        y0 = self.__y - TREE_NODE_RADUIS
        x1 = self.__x + TREE_NODE_RADUIS
        y1 = self.__y + TREE_NODE_RADUIS
         
        return self.__canvas.create_oval(x0, y0, x1, y1,fill=CIRCLE_COLOR_NORMAL)

    def mark_active(self):
        self.__canvas.itemconfig(self.__id, fill=ACTIVE_NODE_COLOR)

    def mark_visited(self):
        self.__canvas.itemconfig(self.__id, fill=VISITED_NODE_COLOR)

    def mark_fringe(self):
        self.__canvas.itemconfig(self.__id, fill=FRINGE_NODE_COLOR)
    
    def mark_goal_path(self):
        self.__canvas.itemconfig(self.__id, fill=GOAL_PATH_COLOR)

    def get_parent(self):
        return self.__parent


class TreeNode(TreeNodeDrawing):

    
    def __init__(self,treecanvas,level,parent,left,right,node,value=0) -> None:
        super(TreeNode,self).__init__(treecanvas,level,parent,left,right,TreeNode)
        self.__node = node
        self.value = value   
    

    def __lt__(self, other):
        return self.value < other.value

    def expand_node(self):

        if self.__node.adj:
            super(TreeNode,self).add_children(self.__node.adj)
            children = super(TreeNode,self).getchildren()
            for child in children:
                child.mark_fringe()
    
    def get_adj(self):
        return self.__node.adj

    def get_node_connection_weight(self,index):
        return self.__node.lines_out[index]
    
    def get_node_heurastic(self):
        return self.__node.heurastic

    def is_goal(self):
        return self.__node.is_goal()
    
    def mark_active(self):
        super(TreeNode,self).mark_active()
        self.__node.mark_active()

    def mark_visited(self):
        super(TreeNode,self).mark_visited()
        self.__node.mark_visited()
    
    def mark_fringe(self):
        super(TreeNode,self).mark_fringe()
        self.__node.mark_fringe()
    
    def mark_goal_path(self):
        super().mark_goal_path()
        self.__node.mark_goal_path()

    def is_visited(self):
        return self.__node.visited
    
    def path_to_root(self,mark=True):
        parent = self.get_parent()
        if mark:
            self.mark_goal_path()
        if parent:
            return parent.path_to_root() + "-->" + self.__node.label  
        else:
            return self.__node.label