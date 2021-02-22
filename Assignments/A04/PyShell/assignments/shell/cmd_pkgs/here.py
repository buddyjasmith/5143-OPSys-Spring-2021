'''
Name: <<
Usage: command << [filepath]
    This operator works, but under very strict conditions. [command] << [filepath]. 
    A valid file path must be passed after the << operator. Input the user enters will then be appended to the file entered.
    The appended file path will be returned in the return status object.
'''

import os
from os.path import abspath
import sys

from cmd_pkgs.return_status import ReturnStatus
def here(args, cwd):
    '''
    :Name:           here
    :Usage:          << [filepath]
    :Description:    the here command opens a temporary editor and appends that information to the file passed 
    :                via the command line. The user must
    '''
    rs = ReturnStatus()
    rs.set_cwd(cwd)
    eof = ''.join(args)
    expression = ''
    exp_list = []

    abs_path = os.path.abspath(os.path.join(cwd,eof))
    print(abs_path)
    if os.path.exists(abs_path):
        sys.stdout.write(f'Type  \'exit\' to exit heredoc\n')
        sys.stdout.flush()
        while (expression != 'exit'):
            exp_list.append(str(expression))
            expression = input('heredoc <<  ')
   
        total_express = '\n'.join(exp_list)
        with open(abs_path,'a') as myfile:
            myfile.write(total_express)
        rs.set_return_status(1)
        rs.set_return_values(abs_path)
        return rs
    else:
        rs.set_return_status(0)
        rs.set_return_values('Invalid path\n')
        return rs
   