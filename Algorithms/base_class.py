# from abc import abstractmethod
import threading
import time


class Algorithm(threading.Thread):

    def __init__(self, inital_node,success_callback,failure_callback ,*args, **kwargs):
        super(Algorithm, self).__init__(*args, **kwargs)
        self.__flag = threading.Event() # The flag used to pause the thread
        self.__flag.set() # Set to True
        self.__running = threading.Event() # Used to stop the thread identification
        self.__running.set() # Set running to True
        self.current_node = inital_node
        self.fringe = []
        self.__failure_callback = failure_callback
        self.__success_callback = success_callback
        self.current_node.mark_active()
        
    
    def expand_node(self):

        '''
        normal implementation to expand node override it when you need
        note : this function expand the node in self.current_node variable. So , loop using this file 
        '''
        self.current_node.expand_node()

        children = self.current_node.getchildren()
        for child in children:
            self.fringe.append(child) 
        
        
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
            self.current_node.mark_active()
            time.sleep(1)
            while self.current_node.is_visited():
                time.sleep(1)
                self.__flag.wait()
                self.current_node.mark_already_visited()
                self.current_node = self.fringe.pop(0)
                self.current_node.mark_active()
        except :
            self.current_node = None
            
    
    def run(self):
        
        while self.__running.is_set() and self.current_node: #  checking if the user terminates the thread or not and checking if the self.current_node = None means fringe is empty and no goal
             
            if(self.check_node()): # check if node is goal or not
                self.current_node.mark_visited()
                self.__success_callback(self.current_node.path_to_root(True))
                return
            self.__flag.wait() # used for pause and resume
            self.expand_node() # expand node
            self.current_node.mark_visited()
            time.sleep(1)
            self.__flag.wait() # used for pause and resume
            self.pick_node() # pick new node from the fringe
            time.sleep(2)
        self.__failure_callback()

    def pause(self):
        self.__flag.clear() # Set to False to block the thread

    def resume(self):
        self.__flag.set() # Set to True, let the thread stop blocking

    def stop(self):
        self.__flag.set() # Resume the thread from the suspended state, if it is already suspended
        self.__running.clear() # Set to False


class BreadthSearchFirst(Algorithm):
    pass