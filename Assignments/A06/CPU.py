import time
from State import State
from ReadyQueue import ReadyQueue
from concurrent.futures import ProcessPoolExecutor
from copy import deepcopy
import sys

class CPU:
    '''
    :Class:             CPU
    :Author:            Buddy Smith
    :Description:       Act as a CPU in a computer scheduling simulation
    :Remarks:           None
    :Data Members:      state: State Object (Enum)
    :                   process: Current process Object
    :                   Quantum: current cpu burst of process object
    :                   max_time: time quantum for Round Robin, default sys.maxsize
    :                   MAX_TIME_REF: constant used for resetting max_time in round robin
    :Methods:           set_process: set current process for processing
    :                   regular computation: computation to be used with SJFS, FCFS, Priority
    :                   rr_computation: special method for Round Robin processing
    :                   perform_computation: delegates computation to correct function for 
    :                                        scheduling algorithm
    '''
    def __init__(self, max_time):
        '''
        :method             constructor
        :params             max_time: max_time quantum
        :description        sets default values of class, state is set to ready
        :                   max_time is set, default max_time i sys.maxsize
        :returns            na
        :todo:              none
        '''
        
        self.state = State(State.READY)
        self.process = None
        self.quantum = None
        self.max_time = max_time
        self.MAX_TIME_REF = deepcopy(self.max_time)
    def set_process(self, process, logger):
        '''
        :method:            set_process
        :params:            process: cpu current process 
        :                   logger: system logger
        :description:       sets the current process to the passed value
        :                   quantum is set to the first value of cpu bursts
        :
        '''
        logger.info(f'SEtting new process for cpu to P{process.id} with a length of cpu_bursts of {len(process.cpu_bursts)} Quantum{process.cpu_bursts[0]}')
        self.state = State.RUNNING

        self.process = process
        self.process.status = State.RUNNING
        self.quantum = process.cpu_bursts[0]
        self.max_time = self.MAX_TIME_REF
       
    def regular_computation(self,logger):
        '''
        :method:            regular_computation
        :params:            logger: system logger
        :description:       method will be called by perform computations as 
        :                   long as the scheduling algo is not round robin.
        :                   When MAX_TIME_REF is not equal to sys.maxsize
        '''
        if self.quantum and self.quantum > 1:    
            self.quantum -= 1
            logger.info(f'P{self.process.id} burst processed.  New time: {self.quantum}')
            if self.quantum != 0:
                return None
        else:
            #lenth of self.quantum == 1, burst finished
            logger.info(f'Return P{self.process.id} to Computer')
            self.state = State.TERMINATED
            p = deepcopy(self.process)
            p.cpu_bursts.pop(0)
            p.status = State.WAITING if p.io_bursts else State.READY if p.cpu_bursts else State.TERMINATED
            logger.info(f'New State of P{p.id} is {p.status}')
            if len(p.cpu_bursts) == 0:
                p.cpu_bursts = None
            self.process = None
            self.quantum = None
            return p
    def rr_computation(self,logger):
        '''
        :method:            rr_computation
        :params:            logger: system logger
        :description:       computation method for round robin.  Will only 
        :                   compute as long as max_time != 0.  Process will 
        :                   be returned to the ready queue. if the quantum is 
        :                   finished, the process is returned with waiting state
        :                   to be passed to io.
        :return             None:  Process hass not reaced end of quantum or max_time
        :                          = 0.
        :                   Process:  processing complete
        '''
        if ((self.quantum) and (self.quantum > 1)) and (self.max_time != 0):
            #subtract one from self.quantum unless max_time reaches zero
            self.quantum -= 1
            self.max_time -= 1
            logger.info(f'P{self.process.id} burst processed. Old Time:{self.quantum +1} New time: {self.quantum} New RR Time: {self.max_time}')
            # a return of none tells computer process is not complete or max time has not been reached
            return None
        else:
            #Either self.quantum <= 1 or self.max_time == 0
            p = deepcopy(self.process)
            self.process = None             # Reset Current CPU Process after copy
            if self.quantum <= 1:
                #Quantum is finished, decide state of Process
                p.cpu_bursts.pop(0)
                if len(p.cpu_bursts) == 0:
                    p.cpu_bursts = None
                    p.status = State.TERMINATED
                else:
                    p.status = State.WAITING
                self.max_time = self.MAX_TIME_REF
                self.quantum = None
                return p
            elif self.max_time == 0:
                # max_time time was reached, self.quantum was not, return to Ready Queue
                p.cpu_bursts[0] = self.quantum
                p.status = State.READY
                self.quantum = None
                self.max_time = self.MAX_TIME_REF
                return p
            else:
                logger.critical(f'Failed to account for state, process maybe lost')
                logger.critical(f'P{p.id} CPU{p.cpu_bursts} IO{p.io_bursts}')
                logger.critical

    def perform_computation(self,logger):
        '''
        :method:            perform_computation
        :params:            logger : system logger
        :description:       if MAX_TIME_REF is not equal to sys.maxsize, SJFS, FCFS, PRIORITY,
        :                   to be processed. else round robin compuation is called
        '''
        if self.MAX_TIME_REF == sys.maxsize:
            result = self.regular_computation(logger)
        else:
            result = self.rr_computation(logger)
        return result
        ######*******! Fix below for round robin, addjust above
        
        
        
        
        
        
        
            

        
