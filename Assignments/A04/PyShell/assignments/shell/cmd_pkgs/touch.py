'''
Command: touch [path/filename]
Description: creates a path in the given path/filename
'''

from cmd_pkgs.return_status import ReturnStatus
import os

def touch(args, cwd):
    '''
    :Function:    touch
    :Arguments:   args: commands passed via shell 
    :         :   cwd: current working directory of shell
    :Description: creates a file in the path the user selected
    :Bugs:        None
    :Returns:     ReturnStatus object
    '''
    touchpath = args[1]
    touchpath = os.path.abspath(os.path.join(cwd,touchpath))
    print(touchpath)
    rs = ReturnStatus()
    rs.set_cwd(cwd)
    help_flag = [x for x in args if x.startswith('--help')]
    if help_flag:
        rs.set_return_status(1)
        rs.set_return_values(__doc__)
        return rs
    if not os.path.exists(touchpath):
        with open(touchpath, 'w') as fp:
            pass
        rs.set_return_status(1)
        rs.set_return_values(touchpath)
        rs.set_cwd(cwd)
    else:
        rs.set_return_status(0)
        rs.set_return_values(f'Path: {touchpath} exists.')
    return rs