'''
mv [source] [destination]

Description:

SYNTAX
      mv [options]... Source Dest

      mv [options]... Source... Directory

If the last argument names an existing directory, 'mv' moves each other given file into a file with the same name in that directory. 
Otherwise, if only two files are given, it renames the first as the second. It is an error if the last argument is not a directory 
and more than two files are given.
'''
from .arg_parser import ArgParse
from .return_status import ReturnStatus
import os
import shutil
import errno
import sys
from colorama import Fore, Style
def mv(args, cwd):
    '''
    :Function: mv
    :Parameters: args: arguments passed from the command line
    :          : cwd: current working directory of shell.
    :Usage: mv [src] [destination]
    :Returns: ReturnSet object
    :Description: moves a file from one destination to another, original source is moved
    :Problems: nada
    :To-Dos: none
    '''
    args.pop(0)
    rs = ReturnStatus()
    rs.set_cwd(cwd)
    help_flag = [x for x in args if x.startswith('--help')]
    if help_flag:
        rs.set_return_status(1)
        rs.set_return_values(__doc__)
        return rs
    current_dir = cwd
    # Pass empty dict because no arguments required for project
    
    
    
    # check if source and destination were passed
    if len(args) == 2:
        src = os.path.abspath(os.path.join(cwd,args[0]))
        dest = os.path.abspath(os.path.join(cwd, args[1]))
        dest_dir = os.path.dirname(dest)
        if os.path.exists(src) :
            dest_file = os.path.basename(dest)
            if os.path.exists(dest_dir):
                shutil.move(src, dest)
                rs.set_return_status(1)
                rs.set_return_values(dest)
            else:
                rs.set_return_status(0)
                rs.set_return_values(f"Invalid destination path: {dest_dir}")
                
           
        elif not os.path.exists(src):
            rs.set_return_status(0)
            rs.set_return_values(Fore.YELLOW + 'Invalid source:' + Style.RESET_ALL)
            rs.set_return_values(__doc__)
    else:
        rs.set_return_status(0)
        rs.set_return_values('Invalid number of arguments: \n')
        rs.set_return_values(__doc__)
    return rs
    

        
    
    
