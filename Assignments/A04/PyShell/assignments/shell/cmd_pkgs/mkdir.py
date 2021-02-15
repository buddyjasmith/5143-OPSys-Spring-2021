"""
    
NAME:  mkdir
Usage: mkdir [path]
mkdir - make a new directory in the path supplied by user

"""
from colorama import Fore, Style
import os
import sys
import errno
from cmd_pkgs.arg_parser import ArgParse
from cmd_pkgs.return_status import ReturnStatus
def mkdir(args, cwd):
    '''
    :Function: mkdir
    :Parameters: args: arguments passed by shell
    :          : cwd: current working directory
    :Usage: mkdir [futurepath]
    :Returns: ReturnStatus object
    :Description: makes a new directory as passed by the user.
    :Problems: nada
    :To-Dos: none
    '''
    rs = ReturnStatus()
    rs.set_cwd(cwd)
    if not args[1:]:
        rs.set_return_status(0)
        rs.set_return_values('New directory path not given in argument')
        return rs
    elif args[1:]:
        new_path = os.path.abspath(os.path.join(cwd,args[1]))
        
        if os.path.exists(new_path):
            rs.set_return_status(0)
            rs.set_return_values('Path Already Exists.')
            #sys.stdout.write(Fore.RED + '\nPath already exists. \n' + Style.RESET_ALL)
            #sys.stdout.flush()
            return rs
        else:
            
            os.mkdir(new_path)
            rs.set_return_status(1)
            rs.set_return_values(new_path)
            #sys.stdout.write('\n' + new_path +'\n')
            #sys.stdout.flush()
            return rs
        
            
            