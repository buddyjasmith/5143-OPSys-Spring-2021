'''
Name
    history
Usage: history
Returns a list of items the user has executed in the pyshell.
The user can append an item of the list with ! to call that line from 
history.
ex: !1 - returns the first command from the history list

'''
import sys
import os
from .return_status import ReturnStatus
path = os.path.abspath('cmd_pkgs/history.txt')
def history(args, cwd):
    '''
    :Function: history
    :Parameters: args: arguments passed from shell.py 
    :          : cwd: current working directory of the shell
    :Usage: history
    :Returns: ReturnStatus object containing a list

    :Description: the function returns a list of all entered commands executed
    :           : in PyShell to be printed to screen. Not to be confused with
    :           : get_history() that returns an actual list
    :Problems: no
    :To-Dos: none
    '''
    rs = ReturnStatus()
    rs.set_return_status(1)
    rs.set_cwd(cwd)
    
    print(path)
    with open(path,'r') as my_file:
        count = 0
        for line in my_file:
            count = count + 1
            line = str(f'{count}: {line}')
            rs.set_return_values(line)
        sys.stdout.flush()
    return rs
def get_history():
    '''
    :Function: get_history()
    :Parameters: none
    :Usage: not a command function
    :Returns: list of executed commands in terminal
    :Description: opens history.txt and returns items in file as a list
    :Problems: none
    :To-Dos: none
    '''
    hist_list = []
    
    with open(path,'r') as my_file:
        for line in my_file:
            
            hist_list.append(line.strip())
    return hist_list

def set_history(new_list):
    '''
    :Function: set_history
    :Parameters: new_list: list of updated history
    :Usage: not a command function
    :Returns: none
    :Description: functions opens history.txt and overwrites contents
    :           : with the new list
    :Problems: none
    :To-Dos: none
    '''
    with open(path,'w') as file:
        for item in new_list:
            file.write(str(item + '\n'))


