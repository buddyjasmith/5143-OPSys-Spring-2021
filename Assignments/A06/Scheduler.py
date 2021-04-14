from abc import ABC, abstractmethod
from typing import Type, List
from Process import Process
class Scheduler(ABC):
    '''
    :Class          Scheduler
    :Description    Abstract class to be utilized by the
    :               scheduler child methods
    '''
    @abstractmethod
    def __init__(self):
        pass
    @abstractmethod
    def set_schedule(self):
        pass
