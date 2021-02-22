'''
NAME
    who - sorts files
SYNOPSIS
    who [options] [filename]
DESCRIPTION
    displays users who are currently logged on.
'''
import getpass
import os
#from cmd_pkgs.arg_parser import ArgParse
#import pwd
import sys
from cmd_pkgs.return_status import ReturnStatus
def who(args, cwd):
    '''
                   :Function:      who
                   :Usage:         who OPTION... [FILE]...
                   :Author:        Buddy Smith & Leila Kalantari
                   :Parameters:    args: parameters from command line
                   :               cwd: current working directory
                   :Description:   displays users who are currently logged on.
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
    rs.set_return_status(1)
    rs.set_return_values(f'USER with os.getuid: {str(os.getuid())}\n')  # real user id
    rs.set_return_values(f'USER using getpass: {str(getpass.getuser())}\n') # login name of user
    return rs
#sys.stdout.write(f'USER with os.getuid: {os.getuid()}\n')  # real user id
#sys.stdout.write(f'USER using getpass: {getpass.getuser()}\n')  # login name of user