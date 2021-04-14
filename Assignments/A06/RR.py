from Scheduler import Scheduler
class RR(Scheduler):
    '''
    :class:             RR (Round Robin)
    :parent:            Scheduler    
    '''
    def __init__(self, quantum):
        self.quantum = quantum
  
    def set_schedule(self, rq, process, logger, time):
        '''
        :method:            set_schedule
        :params:            rq: ReadyQueue Object
        :                   process: Process oject to be inserted
        :                   logger: system logger
        :                   time: system.time
        :Description:       the process is appended to the end of the queue.
        :                   Not alot of scheduling takes place here.  Quantum
        :                   is utilized in cpu
        '''
        rq.put(process, logger)
        
       
       