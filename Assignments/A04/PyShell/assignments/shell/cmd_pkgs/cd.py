'''
NAME
    cd - Change the shell working directory.

SYNOPSIS
    cd  [dir]

DESCRIPTION
    Change the shell working directory.

    Change the current directory to DIR.  The default DIR is ~
'''
import traceback
import os
import sys
from cmd_pkgs.return_status import ReturnStatus
from colorama import Fore, Style
from cmd_pkgs.arg_parser import ArgParse

def cd(args, cwd):
    '''
    :Function:      cd
    :Usage:         cd [destination]
    :Author:        Buddy Smith
    :Parameters:    args: parameters from command line
    :               cwd: current working directory
    :Description:   the function changes the current directory of the OS to the passed value.
    :               If no value is given, the path is changed to the users home directory
    :Todo:          Test more
    :Returns:       Returns the ReturnStatus object consisting  of status, return values, and the cwd
    :Bugs:          None at this time
    '''
    
    sys.stdout.flush()
    
    rs = ReturnStatus()
    rs.set_cwd(cwd)
    ap = ArgParse(args, {}, cwd, __doc__)
    change_path = ap.get_directories()
    flags = ap.get_flags()
    help_flag = [x for x in args if x.startswith('--help')]
    if help_flag:
        rs.set_return_status(1)
        rs.set_return_values(str(__doc__))
        rs.set_cwd(cwd)
        return rs
    temp_path = ''
   
    if len(args) == 1:
        # No arguments after cd were given...change to home directory by default
        path = os.path.expanduser('~')
        os.chdir(path)
        rs.set_cwd(path)
        temp_path = str(path)
        rs.set_return_status(1)
    elif len(args) == 2 and change_path:
        # two arguments were, given and argparser verified path existed
        temp_path = change_path[0]
        if os.path.exists(temp_path):
            os.chdir(temp_path)
            rs.set_cwd(temp_path)
            rs.set_return_status(1)
        else:
            # Just in case argparser messed up at this point 
            rs.set_return_status(0)
            rs.set_return_values(f'Invalid  Path: ')

    else:
        temp_path += Fore.YELLOW + 'Too many parameters given\n' + Style.RESET_ALL
        temp_path += __doc__
        rs.set_return_status(0)
        rs.set_cwd(cwd)
        
   

        
    rs.set_return_values(temp_path)
  
    return rs