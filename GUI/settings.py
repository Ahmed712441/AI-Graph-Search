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
   
    normal  = 1           # neither circle nor line is clicked 
    circle = 2           # circle is clicked
    line   = 3           # line is clicked

    def __init__(self):
        self.__state = Mouse_state.normal
        self.callback = None    

    def set_callback(self,callback):
        self.callback = callback


    def set_state(self,new_state):
        
        if self.callback :
            self.callback()
            self.__state = new_state
        else:
            self.__state = new_state

    def get_state(self):
        
        return self.__state
    

mouse = Mouse_state()

RADUIS = 40

CIRCLE_COLOR_NORMAL = "#0f0"
LINE_COLOR_NORMAL = "#fff"
CIRCLE_COLOR_SELECTED = "blue"
LINE_COLOR_SELECTED = 'black'
CANVAS_BACKGROUND_COLOR = 'grey'