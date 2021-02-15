

from cmd_pkgs.return_status import ReturnStatus
import os
import sys
import csv
def file_redirect(args, cwd):
    '''
    :Function:      file_redirect
    :parameters:    args: arguments passed from command line
    :               cwd: current working directory of shell
    :Usage:         [cmd] > [filename]
    :Description:   The command moves the output of whatever command parsed before the 
    :               chain operator, and and appends it to the filename given by the
    :               user in args.
    '''
   
    rs = ReturnStatus()
    rs.set_cwd(cwd)
    args.pop(0)    # remove > symbol from args
    file = args[0] # 
    args.pop(0)    # remove file name from args before joining
    contents = ''.join(args)
    
    abspath = os.path.abspath(os.path.join(cwd, file))
    try:
        with open(abspath, 'w+') as file:
            file.writelines(contents)
        rs.set_return_status(1)
        rs.set_return_values(abspath)
    except EnvironmentError as ex:
        rs.set_return_status(0)
        rs.set_return_status('Inavlid parameters/Environments Error:')
        rs.set_return_values(__doc__)

   
    
    return rs
def file_append(args,cwd):
    '''
    :**************************************************************************
    :Function:      file_append
    :Arguments:     args: arguments passed by the user from the command line
    :               cwd: current working directory of the terminal
    :Usage:         [cmd] >> [filepath]
    :Description:   the function appends the return of one command to the user
    :               designated file path
    :**************************************************************************
    '''
   
    rs = ReturnStatus()
    rs.set_cwd(cwd)
    args.pop(0)    # remove > symbol from args
    file = args[0] # 
    args.pop(0)    # remove file name from args before joining
    contents = ''.join(args)
    abspath = os.path.abspath(os.path.join(cwd, file))
    if os.path.exists(abspath):
        try:
            with open(abspath, 'a') as f:
                f.writelines(contents)
            rs.set_return_status(1)
            rs.set_return_values(abspath)
        except EnvironmentError(IOError, OSError, FileNotFoundError) as ex:
            rs.set_return_status(0)
            rs.set_return_status('Inavlid parameters/Environments Error:')
            rs.set_return_values(file_append.__doc__)
    else:
        rs.set_return_values('Invalid file path given for >>, try > instead or check path')
        rs.set_return_values(file_append.__doc__)
        rs.set_return_status(0)
              
    return rs
