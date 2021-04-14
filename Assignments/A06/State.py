from enum import Enum
class State(Enum):
    '''
    :Purpose:           to be used to represent states of 
    :                   various processes and io devices, etc
    '''
    NEW = 0
    READY = 1
    RUNNING = 2
    WAITING = 3
    TERMINATED = -1