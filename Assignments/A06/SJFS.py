from Scheduler import Scheduler
from typing import Type, List
from Process import Process
from collect import collect
from ReadyQueue import ReadyQueue
class SJFS(Scheduler):
    '''
    :class:             SJFS
    :members:           na
    :methods:           set_schedule
    :description:       Shortest job first algorithm
    '''
    def __init__(self):
        pass   

    def set_schedule(self, rq, process, logger, time):
        '''
        :method:        set_schedule
        :params:        rq: ReadyQueue object
        :               logger: system logger
        :               process: process to be inserted into ready_queue
        :               time: system.time
        :description:   the set schedule object takes a process passed by
        :               params and inserts it in the readyqueue.  Immdediately
        :               afterwards, readyqueue is then sorted by the first
        :               cpu_burst in each process, ensuring the shortest
        :               algorithms at the beginning at the list.  Ordered is 
        :               maintained with each insertion into the readyqueue
        '''

        rq.put(process, logger)
        rq.ready_queue.sort(key=lambda x: x.curr_burst)
       
       

