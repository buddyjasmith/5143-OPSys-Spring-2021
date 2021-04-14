import time
from State import State
class Process:
    '''
    :class              Process
    :constructor        parameterized
    :data members       id: id of proces
    :                   N: number of cpu bursts
    :                   cpu_bursts: list()
    :                   io_bursts: list()
    :                   at: arrival time of process
    :                   proc_done: time cpu bursts completed
    :                   io_done: time io completed
    :                   curr_burst: current cpu burst
    :                   curr_io: current io burst
    :                   status: ENUM STATE
    '''
    def __init__(self,at, id_num,priority, N, cpu_burst_durations, io_burst_durations):
        #! Parameterized Constructor
        self.id = id_num
        self.N = N
        self.cpu_bursts = cpu_burst_durations
        self.io_bursts = io_burst_durations
        self.arrival_time = at
        self.curr_burst= self.cpu_bursts[0]
        self.curr_io = self.io_bursts[0]
        self.proc_done = 0
        self.io_done = 0
        self.arrival_order = 0
        self.io_wait_time = 0
        self.cpu_wait = 0
        self.io_wait = 0
        self.status = State.NEW
        self.priority = priority
        self.start_time = -1
        self.running_time = 0
    def __repr__(self):
        '''
        :method:            __repr__
        :params:            na
        :description:       to string method for process object
        '''
        id = f'ProcessID: {self.id}\n\t'
        priority =f'Priority: {self.priority}\n\t'
        at= f'ArrivalTime: {self.arrival_time}\n\t'
        start = f'Start Time: {self.start_time}\n\t'
        cpu_done=f'Processing done by: {self.proc_done}\n\t'
        io_done = f'IO done by: {self.io_done}\n\t'
        cpu_wait_time = f'CPU Wait Time: {self.cpu_wait}\n\t'
        io_wait_time = f'IO Wait time: {self.io_wait}\n\t'
        r_value = f'{id} {priority} {at} {start} {cpu_done} {io_done} {cpu_wait_time} {io_wait_time}'
        return r_value
        
    def set_curr_burst(self):
        '''
        :method:            set_curr_bursts
        :params:            none
        :description:       sets curr_bursts to the first value of cpu_bursts
        '''
        if self.cpu_bursts:
            self.curr_burst = self.cpu_bursts[0]
    def set_io_done(self, time):
        '''
        :method:            set_io_done
        :params:            time: time of system clock
        :description:       set once io processing has been completed
        '''
        self.io_done = time
    def set_proc_done(self, time):
        '''
        :method:            set_proc_done
        :params:            time: value of system clock
        :description:       proc_done is set to the value of the system clock
        :                   to be used when all processes have completed
        '''
        self.proc_done = time
    def set_status(self, state):
        '''
        :method:            set_status
        :params:            state: ENUM State OBJECT
        :description:       setter method for the status member
        '''
        self.status = state