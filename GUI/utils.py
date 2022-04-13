class OverlapException(Exception):

    def __init__(self,message="Can't place the node as it overlaps with another node"
                ,title="Overlaping Error"):
        self.message = message
        self.title = title
        super().__init__(self.message)
    
    def __str__(self) -> str:
        return self.message

class DuplicateConnectionException(Exception):

    def __init__(self,message="This connection already exists"
                ,title="Duplicate Connection Error"):
        self.message = message
        self.title = title
        super().__init__(self.message)
    
    def __str__(self) -> str:
        return self.message


class Mouse_state:
   
    normal  = 1          # neither circle nor line is clicked 
    circle = 2           # circle is clicked
    line   = 3           # line is clicked
    initial_node = 4     # initial node clicked
    goal_node = 5        # goal node clicked
    disabled = 6         # clicks is disabled

    def __init__(self):
        self.__state = Mouse_state.normal
        self.callback = None    
        self.__root = None

    def set_root(self,root):
        self.__root = root

    def set_callback(self,callback):
        self.callback = callback

    def __reset_cursor(self):
        if (self.__state == Mouse_state.goal_node):
            self.__root.config(cursor="target")
        elif(self.__state == Mouse_state.initial_node):
            self.__root.config(cursor="spider")
        elif(self.__state == Mouse_state.line):
            self.__root.config(cursor="plus")
        elif(self.__state == Mouse_state.circle):   
            self.__root.config(cursor="cross")
        else:
            self.__root.config(cursor="arrow")
            

    def set_state(self,new_state):
        
        if self.callback :
            self.callback()
            self.__state = new_state
        else:
            self.__state = new_state
        self.__reset_cursor()

    def get_state(self):
        
        return self.__state

mouse = Mouse_state()