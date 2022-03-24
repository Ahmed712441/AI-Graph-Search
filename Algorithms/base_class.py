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
        # self.visited = []
    
    def expand_node(self):

        '''
        normal implementation to expand node override it when you need
        note : this function expand the node in self.current_node variable. So , loop using this file 
        '''
        
        for node in self.current_node.adj:
            node.mark_in_fringe()
        
        self.fringe += self.current_node.adj
        
        
    def check_node(self):
        
        '''
        normal implementation to check if node is goal or not override it when you need
        ''' 
        return self.current_node.is_goal()


    def pick_node(self):

        '''
        normal implementation to pick new node        
        ''' 
        try:
            self.current_node = self.fringe.pop(0)
        except:
            self.current_node = None

    
    def run(self):
        
        while self.__running.is_set(): # checking if the user terminates the thread or not
            while self.current_node: # checking if the self.current_node = None means fringe is empty and no goal
                self.__flag.wait() # used for pause and resume
                self.current_node.mark_active() # change node color to active color which indicates that it is processed
                if(self.check_node()): # check if node is goal or not
                    print("goal found") # this will be changed to be displayed on label
                    return # finish the thread
                self.expand_node() # expand node
                self.current_node.mark_visited() # change node color to visited node
                self.pick_node() # pick new node from the fringe
                

    def pause(self):
        self.__flag.clear() # Set to False to block the thread

    def resume(self):
        self.__flag.set() # Set to True, let the thread stop blocking

    def stop(self):
        self.__flag.set() # Resume the thread from the suspended state, if it is already suspended
        self.__running.clear() # Set to False
