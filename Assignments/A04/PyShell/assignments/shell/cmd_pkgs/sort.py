'''
NAME
    sort - sorts files
SYNOPSIS
    sort [-C] [file]
Flags: -C: sorts contents passed rather a file
DESCRIPTION
    sorts the contents of a text file, line by line.
'''
from cmd_pkgs.arg_parser import ArgParse
from cmd_pkgs.return_status import ReturnStatus
from colorama import Fore, Style
def sort(args, cwd):
    '''
    :Function: sort
    :Parameters: args: arguments passed by user
    :          : cwd: current working directory of shell
    :Usage: sort [file]
    :Returns: ReturnStatus object
    :Description: sorts a files contents
    :Problems: none
    :To-Dos: add functionality to sort other values such as just conetents if passed
    :      : add more error testing.  This requires adjusting argparser
    '''
    print(args)
    
    print('Sort is called')
    content_flag = [x for x in args if '-C' in x]
    rs = ReturnStatus()
    if content_flag:
        print('Content was detected')
        arguments = args[2:]
        
        arguments.sort()
        string = '\n'.join(arguments)
        
        rs.set_return_status(1)
        rs.set_return_values(string)
        rs.set_cwd(cwd)
        
        return rs
    arg_parse = ArgParse(args, {}, cwd, __doc__)
    flags = arg_parse.get_flags()
    
    rs.set_cwd(cwd)
    help_flag = [x for x in args if x.startswith('--help')]
    if help_flag:
        rs.set_return_status(1)
        rs.set_return_values(__doc__)
        return rs
    directories = arg_parse.get_directories()
    lines = []
    
    rs.set_return_status(1 if directories else 0)
    for p in directories:
        try:
            with open(p, "r+") as f:
                lines = f.read().splitlines()
            lines.sort()
            rs.set_return_values('\n'.join(lines))
        except FileNotFoundError:
            rs.set_return_status(0)
            rs.set_return_values('Invalid file path')
            return rs
        except Exception:
            rs.set_return_values('Something went wrong')
            rs.set_return_status(0)
            return rs
        return rs