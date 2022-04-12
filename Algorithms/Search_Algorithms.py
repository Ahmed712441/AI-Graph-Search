from Algorithms.base_class import BaseAlgorithm
import time

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
        except Exception as e:
            print(e)
            self.current_node = None

class DepthLimitedSearch(DepthFirstSearch):
    
    def __init__(self, inital_node,success_callback,failure_callback,*args, **kwargs):
        
        self.__limit =  kwargs.pop('limit')
        super(DepthLimitedSearch,self).__init__(inital_node,success_callback,failure_callback ,*args, **kwargs)
        

    def expand_node(self):
        if self.current_node.get_level() < self.__limit:
            super(DepthLimitedSearch,self).expand_node()
        
class IterativeDeepeningSearch(DepthLimitedSearch):
    pass


class UniformCostSearch(BaseAlgorithm):
    pass


class GreedyBestFirstSearch(BaseAlgorithm):
    pass

class AStarSearch(BaseAlgorithm):
    pass


