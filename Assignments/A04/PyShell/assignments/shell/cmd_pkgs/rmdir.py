'''
Name
    rmdir - remove empty directories
Synopsis
    rmdir [OPTION]... DIRECTORY..
Flags
    - 'f' Force deletion of non empty directory
    - 'r' recursively delete contents of non empty directory
'''
from shutil import rmtree
from cmd_pkgs.arg_parser import ArgParse
from cmd_pkgs.return_status import ReturnStatus
from colorama import Fore, Style
import sys
import os
cmd_dict ={
    'f': False,
    'r': False,
}
def rmdir(args, cwd):
    '''
    :Function: rmdir
    :Parameters: args: arguments passed from the shell
    :          : cwd: current working directory of shell
    :Usage: rm [path]
    :Returns: ReturnStatus object
    :Description: removes a non empty directory.  if the directory
    :           : has contents, the -r or -f must be passed to forec
    :           : deletion
    :Problems: none
    :To-Dos: ??
    '''
    rs = ReturnStatus()
    rs.set_cwd(cwd)
    ap = ArgParse(args, cmd_dict, cwd, __doc__)
    flags = ap.get_flags()
    directories = ap.get_directories()
    help_flag = [x for x in args if x.startswith('--help')]
    if help_flag:
        rs.set_return_status(1)
        rs.set_return_values(__doc__)
        return rs
    for dir in directories:
        if len(os.listdir(dir)) == 0:
            # make sure directory is empty, if so delete
            rs.set_return_status(1)
            rs.set_return_values(f'Deleted path: {dir}\n')
            rmtree(dir)
        elif 'r' in flags or 'f' in flags:
            # directory is not empty, check if r or f flags, if so allow delete
            rs.set_return_status(1)
            rs.set_return_values(f'Deleted path: {dir}\n')
            rmtree(dir)
        else:
            # directory is not empty, no flags were passed, do not delete
            rs.set_return_status(0)
            rs.set_return_values(Fore.RED + '\nNon Empty Directory\n' + Style.RESET_ALL)
            rs.set_return_values(__doc__)

        sys.stdout.flush()
        return rs