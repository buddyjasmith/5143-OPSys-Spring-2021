'''
Name: 
    pwd
Description:
    Print the current directory of the user
'''
import sys
import os
from .return_status import ReturnStatus
def pwd(args, cwd):
    '''
    :Function: pwd
    :Parameters: args: arguments passed by user
    :          : cwd: current working directory of shell
    :Usage: pwd
    :Returns: ReturnStatus object  
    :Description: returns the current working directory of pyshell
    :Problems: nada
    :To-Dos: none
    '''
    rs = ReturnStatus()
    rs.set_return_status(1)
    rs.set_cwd(cwd)
    rs.set_return_values(cwd)
    return rs