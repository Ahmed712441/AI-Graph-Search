from settings import *

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

    


    def expand(self):
        
        num_of_nodes = len(self.__node.adj)
        if(num_of_nodes % 2 == 0):

            bound = num_of_nodes // 2
            counter = 0
            y = (self.__level+1) * TREE_VER_DISTANCE
            for i in range(-bound,bound+1):
                if i < 0:
                    x = self.__x + i*TREE_NORMAL_HOR_DISTANCE - RADUIS  
                    TreeNode(self.__treecanvas,self.__node.adj[counter],self.__level+1,self,x,y) 
                    counter += 1
                elif i > 0:
                    x = self.__x + i*TREE_NORMAL_HOR_DISTANCE + RADUIS  
                    TreeNode(self.__treecanvas,self.__node.adj[counter],self.__level+1,self,x,y)
                    counter += 1

        else:
            
            bound = num_of_nodes // 2
            counter = 0
            y = (self.__level+1) * TREE_VER_DISTANCE
            for i in range(-bound,bound+1):
                if i < 0:
                    x = self.__x + i*TREE_NORMAL_HOR_DISTANCE - RADUIS  
                    TreeNode(self.__treecanvas,self.__node.adj[counter],self.__level+1,self,x,y) 
                elif i > 0:
                    x = self.__x + i*TREE_NORMAL_HOR_DISTANCE + RADUIS  
                    TreeNode(self.__treecanvas,self.__node.adj[counter],self.__level+1,self,x,y)
                else:
                    TreeNode(self.__treecanvas,self.__node.adj[counter],self.__level+1,self,self.__x,y)