import time
from enum import Enum
class State(Enum):
    NEW = 0
    READY = 1
    RUNNING = 2
    WAITING = 3
    TERMINATED = -1

class IO:
    def __init__(self, type_of=None):
        self.state = State(State.WAITING)
        self.process = None
        self.quantum = None
    def set_process(self, process, logger):
        logger.info(f'P{process.id} recieved by IO.  IO-Time: {process.io_bursts[0]}')
        self.process = process
        self.quantum = process.io_bursts[0]
        self.process.status = State.RUNNING
       
     
    def process_io(self, logger):
        if self.quantum >=1:
            logger.info(f'P{self.process.id} processing IO.  Old Quantum: {self.quantum} New Quantum: {self.quantum -1}')
            self.quantum -= 1
            
            return None
        else:
            logger.info(f'P{self.process.id}: Completed IO Burst')
            p = self.process
            p.io_bursts.pop(0) #first io burst completed
            if len(p.io_bursts) == 0:
                p.io_bursts = None
            p.status = State.READY
            self.process = None
            logger.info(f'RETURNING P{p.id} to Computer\nWith and IO schedule of {p.io_bursts}')
            return p
        
    def get_io_burst(self):
        pass

    
            

