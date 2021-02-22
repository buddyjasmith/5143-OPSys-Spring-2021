'''
Name: tail
Usage: tail [-n] [paths]
Flags:  -n : number of lines to read
'''

#What is the tail command?
#The tail command is a command-line utility for outputting the last part
# of files given to it via standard input. It writes results to standard
# output. By default tail returns the last ten lines of each file that it is given
import re  # Regular Expression(RE) Syntax AND
import sys
import os
from cmd_pkgs.arg_parser import ArgParse
from cmd_pkgs.return_status import ReturnStatus
from cmd_pkgs.return_status import ReturnStatus

def tail(args, cwd):
    '''
    :Function:      tail
    :Usage:         tail OPTION... [FILE]...
    :Author:        Buddy Smith & Leila Kalantari
    :Parameters:    args: parameters from command line
    :               cwd: current working directory
    :Description:   prints the last few number of lines (10 lines by default)
                    of a certain file, then terminates.
    :Todo:          Test more
    :Returns:       Returns the ReturnStatus object consisting  of status, return values, and the cwd
    :Bugs:          None at this time
    '''
    rs = ReturnStatus()
    rs.set_cwd(cwd)
    help_flag = [x for x in args if x.startswith('--help')]
    if help_flag:
        rs.set_return_status(1)
        rs.set_return_values(__doc__)
        return rs
    args.pop(0) #remove first commands from args
    flags =  [x for x in args if x.startswith('--') or x.startswith('-')]
    args = [x for x in args if not x.startswith('-') or not x.startswith('--')]
    file_paths = args
    n = []
    if '--help' in flags:
        rs.set_return_status(1)
        rs.set_return_values(__doc__)
        return rs
    if  len(flags) == 1:                    # n was passed if flags > 0
        n = flags[0]
        n = int(n)
        n = n * -1                          # get rid of - from args
          
    else:
        n=10
    if n:
        text = []
        lines = []
        for path in file_paths:
            path = os.path.abspath(os.path.join(cwd,path))
            if os.path.exists(path) and os.path.isfile(path):
                with open(path, 'r') as file:
                    lines = file.read().splitlines()
                    numLines = len(lines)
                    for line in lines[(numLines - n):]:
                        text.append(line)
        if text:
            temp = '\n'.join(text)
            rs.set_return_status(1)
            rs.set_return_values(temp)
            return rs
        else:
            rs.set_return_status(0)
            rs.set_return_values(__doc__)
    return rs
    
    
   
    
   
    
    