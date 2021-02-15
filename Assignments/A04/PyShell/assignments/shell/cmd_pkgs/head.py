'''
Name: head
head [option]...[file]
Print the first 10 lines of each FILE to standard output.  With
       more than one FILE, precede each with a header giving the file
       name.

       With no FILE, or when FILE is -, read standard input.

       -n, --lines=[-]NUM
              print the first NUM lines instead of the first 10; with
              the leading '-', print all but the last NUM lines of each
              file
'''
from cmd_pkgs.arg_parser import ArgParse
from cmd_pkgs.return_status import ReturnStatus
import os
import sys
from colorama import Fore, Style
from itertools import islice
head_dict = {
       'n': False,
       }
def head(args, cwd):
    '''
    :Function:      head
    :Usage:         head [n=lines read] [file/directory]
    :Author:        Buddy Smith
    :Parameters:    args: parameters from command line
    :               cwd: current working directory
    :Description:   the function reads the first n lines of the files/directory passed. If n is not
    :               passed, 10 lines will be read and printed to the screen.
    :Todo:          Test more
    :Returns:       Returns the ReturnStatus object consisting  of status, return values, and the cwd
    :Bugs:          None at this time
    '''
    rs = ReturnStatus() # object returned to shell with results
    
    ap = ArgParse(args,head_dict,cwd,__doc__)
    n_flags = [x for x in args if  x.startswith('-')]    # get list of items that start with '-'
    
    head = None
    directories = ap.get_directories()
    if n_flags is None:
           n_flags = 10
    else:
       n_flags = n_flags[0]
       n_flags = int(n_flags[1:])
   
    head_contents=''
    print(directories)
    for dir in directories:
       
       if os.path.isdir(dir):
           directory = os.listdir(dir)
           for file in directory:
              abspath = os.path.abspath(os.path.join(dir,file))
              rs.set_return_values(str(os.path.basename(abspath) + ':\n'))
              if os.path.isfile(abspath):
                  try:
                     with open(abspath) as myfile:
                         head = list(islice(myfile, n_flags))
                  except Exception:
                         rs.set_return_status(0)
                         rs.set_return_values(f'Trouble opening {abspath}')
                  head = ''.join(head)
       if os.path.isfile(dir):
           rs.set_return_values(str(os.path.basename(dir) + ':\n'))
           with open(dir) as myfile:
               head = list(islice(myfile, n_flags))
           head = ''.join(head)        
    rs.set_cwd(cwd)
    
    if head:
           rs.set_return_status(1)
           rs.set_return_values(head)
    else:
           rs.set_return_status(0)
    
    return rs

    