from Algorithms.base_class import BaseAlgorithm
import time
import threading

class BreadthFirstSearch(BaseAlgorithm):
    pass


class DepthFirstSearch(BaseAlgorithm):


    def expand_node(self):

        
        self.current_node.expand_node()
        children = self.current_node.getchildren()
        i = len(children)-1
        while i >=0 :
            self.fringe.append(children[i])
            i-=1 

    def pick_node(self):

        try: 
            self.current_node = self.fringe.pop()
            self.current_node.mark_active()
            time.sleep(1)
            while self.current_node.is_visited():
                time.sleep(1)
                self.get_wait_flag().wait()
                self.current_node.mark_already_visited()
                self.current_node = self.fringe.pop()
                self.current_node.mark_active()
        except :
            
            self.current_node = None

class DepthLimitedSearch(DepthFirstSearch):
    
    def __init__(self, inital_node,success_callback,failure_callback,*args, **kwargs):
        self.__has_unexplored = False
        self.__limit =  kwargs.pop('limit')
        super(DepthLimitedSearch,self).__init__(inital_node,success_callback,failure_callback ,*args, **kwargs)
    
    def set_limit(self,limit):
        self.__limit = limit
        
    def still_unexplored(self):
        return self.__has_unexplored

    def expand_node(self):
        current_level = self.current_node.get_level()
        self.current_node.set_expanded_level(current_level)
        if current_level < self.__limit :
            super(DepthLimitedSearch,self).expand_node()
        else :
            self.__has_unexplored = self.current_node.has_children()
            self.current_node.mark_visited()
        
    def pick_node(self):

        try: 
            self.current_node = self.fringe.pop()
            self.current_node.mark_active()
            time.sleep(1)
            while self.current_node.is_visited() and self.current_node.get_expanded_level() <= self.current_node.get_level():
                time.sleep(1)
                self.get_wait_flag().wait()
                self.current_node.mark_already_visited()
                self.current_node = self.fringe.pop()
                self.current_node.mark_active()
        except :
            self.current_node = None

class IterativeDeepeningSearch(DepthLimitedSearch):
    
    def __init__(self, inital_node,success_callback,failure_callback,*args, **kwargs):
        self.__current_limit =  0
        self.__still_running_flag = threading.Event()
        self.__still_running_flag.set()
        self.__success = success_callback
        self.__treecanvas = inital_node.get_canvas()
        self.__canvas = kwargs.pop('canvas')
        self.__failure = failure_callback
        self.__inital_node = inital_node
        super(IterativeDeepeningSearch,self).__init__(inital_node,self.__on_success,None,limit= self.__current_limit,*args, **kwargs)
    
    def __on_fail(self):
        self.__still_running_flag.clear()
        self.__failure()
            
    def __on_success(self,path):
        self.__still_running_flag.clear()
        self.__success(path)

    def reset(self):
        self.__treecanvas.delete("all")
        self.__canvas.reset()
        time.sleep(1)
        self.__current_limit+=1
        self.set_limit(self.__current_limit)
        self.__inital_node.reset_node()
        self.current_node = self.__inital_node
        
    
    def run(self):
        while True :
            super(IterativeDeepeningSearch,self).run()
            if(self.get_running_flag().is_set()):
                if (self.__still_running_flag.is_set()):
                    if self.still_unexplored() :
                        self.reset()
                    else:
                        self.__on_fail()
                else :
                    return
            else :
                self.__on_fail()
                return


class UniformCostSearch(BaseAlgorithm):
    pass


class GreedyBestFirstSearch(BaseAlgorithm):
    pass

class AStarSearch(BaseAlgorithm):
    pass


