from queue import Queue
from Process import Process
from copy import deepcopy
class ReadyQueue:
    def __init__(self):
        self.ready_queue = list()
        self.finished = list()
        self.current_process = None
        self.curr_burst = None
        self.current_io = None
        self.io_wait_list = list()
    def put(self, process, logger):
        if (process.cpu_bursts == None) and (process.io_bursts == None):
            self.finished.append(process)
            return
        logger.warning(f'P{process.id} CB:{process.cpu_bursts} IO{process.io_bursts}')
        process.curr_burst = process.cpu_bursts[0]
        # process.io_burst = process.io_bursts[0]
        self.ready_queue.append(process)
    def pop(self):
        if len(self.ready_queue) > 0:
            return self.ready_queue.pop(0)
        return None
    def empty(self):
        if len(self.ready_queue) == 0:
            return True
        return False

   
                
            

           
            
   