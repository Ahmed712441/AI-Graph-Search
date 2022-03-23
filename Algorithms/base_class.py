from abc import abstractmethod
import threading

class TreeNode:
    pass


class Algorithm(threading.Thread):

    def __init__(self, inital_node, canvas ,*args, **kwargs):
        super(Algorithm, self).__init__(*args, **kwargs)
        self.__flag = threading.Event() # The flag used to pause the thread
        self.__flag.set() # Set to True
        self.__running = threading.Event() # Used to stop the thread identification
        self.__running.set() # Set running to True
        # self.inital_node = inital_node
        self.current_node = inital_node
        self.canvas = canvas
        self.fringe = []
        self.visited = []
    
    
    def add(self):
        '''
        normal implementation to add expanded nodes to fringe override it in uniform search to add them sorted by weight
        '''
        self.fringe += self.current_node.adj

    def expand(self):
        
        self.add()
        # self.canvas
    

    @abstractmethod
    def run(self):
        pass

    def pause(self):
        self.__flag.clear() # Set to False to block the thread

    def resume(self):
        self.__flag.set() # Set to True, let the thread stop blocking

    def stop(self):
        self.__flag.set() # Resume the thread from the suspended state, if it is already suspended
        self.__running.clear() # Set to False
