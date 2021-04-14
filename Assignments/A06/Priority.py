from Scheduler import Scheduler
from typing import Type, List
from Process import Process
from collect import collect
from ReadyQueue import ReadyQueue
class Priority(Scheduler):
    def __init__(self):
        pass 
    def set_schedule(self, rq, process, logger, time):
        '''
        :method:            set_schedule
        :params:            rq: ReadyQueue Object
        :                   process: Process Object to be inserted
        :                   logger:  system logger
        :                   time: system time
        '''
        rq.put(process, logger)
        rq.ready_queue.sort(key=lambda x: x.priority)
        

       