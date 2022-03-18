RADUIS = 40

class Node:

    def __init__(self,canvas,x,y,label,goal=False):

        self.__adj = [] # carries adjancent nodes
        self.lines_out = [] # carries ids of lines connecting it to other nodes
        self.lines_in = [] # carries ids of lines connecting other node to it 
        self.goal = goal # is this node a goal or not 
        self.canvas = canvas # canvas object helps in drawing on screen
        self.x = x # x coordinate of its center
        self.y = y # y coordinate of its center
        self.label = label # unique label used to identify each node used mainly in GUI 

    def connect_node(self,node):
        
        self.__adj.append(node)
        if(node.y < self.y):
            line_id = self.canvas.create_line(self.x,self.y+RADUIS,node.x,node.y+RADUIS,arrow="last",fill="#fff")
        elif(node.y > self.y):
            line_id = self.canvas.create_line(self.x,self.y-RADUIS,node.x,node.y-RADUIS,arrow="last",fill="#fff")
        elif(node.x > self.x):
            line_id = self.canvas.create_line(self.x+RADUIS,self.y,node.x-RADUIS,node.y,arrow="last",fill="#fff")
        elif(node.x < self.x):
            line_id = self.canvas.create_line(self.x-RADUIS,self.y-RADUIS,node.x+RADUIS,node.y-RADUIS,arrow="last",fill="#fff")


        self.lines_out.append(line_id)
        node.lines_in.append(line_id)
        self.canvas.lower(line_id)


    def __create_circle(self): #center coordinates, radius
        
        x0 = self.x - RADUIS
        y0 = self.y - RADUIS
        x1 = self.x + RADUIS
        y1 = self.y + RADUIS
        overlap = self.canvas.find_overlapping(x0, y0, x1, y1)
        if len(overlap):
            raise Exception("Cann't place this object as it overlaps with another object")
        return self.canvas.create_oval(x0, y0, x1, y1,fill="#0f0")


    def create_node(self):
        self.id = self.__create_circle()
        self.label_id = self.canvas.create_text((self.x, self.y), text=self.label)
        return self.id

    def change_node_color(self):
        
        self.canvas.itemconfig(self.id, fill="red")

    def change_connection_color(self,index):

        self.canvas.itemconfig(self.connections[index], fill="red")

    def delete_node(self):
        
        for item in self.lines_out+self.lines_in:
            self.canvas.delete(item)

        self.canvas.delete(self.id)
        self.canvas.delete(self.label_id)