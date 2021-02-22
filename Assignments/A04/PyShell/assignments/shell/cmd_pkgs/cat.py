'''
NAME:
    cat - 
Flags:
    -d : Cat entire
SYNOPSIS:
    cat  [file],[file1 file2 >file0]
DESCRIPTION:
    display a file and concatenate file1 and file2 to file0
'''
import re  # Regular Expression(RE) Syntax AND
from cmd_pkgs.arg_parser import ArgParse
import os
from colorama import Fore, Style
from cmd_pkgs.return_status import ReturnStatus
cat_flags = {
    'd': False
}
def cat(args, cwd):
    '''
        :Function:      cat
        :Usage:         cat [OPTION] [FILE]...
        :Author:        Buddy Smith & Leila Kalantari
        :Parameters:    args: parameters from command line
        :               cwd: current working directory
        :Description:   display a file and concatenate file1 and file2 to file0
        :Todo:          Test more
        :Returns:       Returns the ReturnStatus object consisting  of status, return values, and the cwd
        :Bugs:          None at this time
    '''
    # If the only parameters are files
    # just print the files out to screen.
    arg_parse = ArgParse(args, cat_flags, cwd, __doc__)
    flags = arg_parse.get_flags()
    help_flag = [x for x in args if x.startswith('--help')]
    

    rs = ReturnStatus()
    rs.set_cwd(cwd)
    if help_flag:
        rs.set_return_status(1)
        rs.set_return_values(str(__doc__))
        return rs
    # if flags:
    #     rs.set_return_status(0)
    #     rs.set_return_values('cat does not support flags at this time')
    #     rs.set_return_values(__doc__)
    directories = arg_parse.get_directories()
    #print(directories)
    num = 0
    files_contents=[]
    for p in directories:
        
        path = os.path.abspath(os.path.join(cwd,p))
       
        if os.path.isdir(path) and 'd' in flags:
           
            directory = os.listdir(path)
            for dir in directory:
                
                files_contents = []
                files_contents.append(str(Fore.GREEN + '\n' + dir + ':' + Style.RESET_ALL))
                current_path = os.path.abspath(os.path.join(cwd,p))
                current_path = os.path.abspath(os.path.join(current_path, dir))
               
                try:
                    with open(current_path, 'r') as file:
                        lines = file.read().splitlines()
                        for line in lines:
                            files_contents.append(str(line ))
                    temp_contents = '\n'.join(files_contents )
                except Exception:
                    rs.set_return_status(0)
                    rs.set_return_values('Trouble reading path.')
                    return rs
                
                rs.set_return_status(1)
                rs.set_return_values(temp_contents)
        elif os.path.isdir(path) and not flags:
            rs.set_return_status(0)
            rs.set_return_values(f'cat: {path} is a directory.')
            rs.set_return_values(f'Use the -d flag to cat entire directory')
            return rs
        else:
            path = os.path.abspath(os.path.join(cwd, p))
            
            if os.path.exists(path):
                try:
                    with open(path, 'r') as file:
                        lines = file.read().splitlines()
                        for line in lines:
                            files_contents.append(line)
                    temp_contents = '\n'.join(files_contents)
                    #print(temp_contents)
                    if temp_contents:
                        rs.set_return_values(temp_contents)
                        rs.set_return_status(1)
                except PermissionError:
                    rs.set_return_values('Invalid permissions:')
                    rs.set_return_status(0)
                    return rs
                except Exception:
                    rs.set_return_values('Unable to open file')
                    rs.set_return_values(0)
                    return rs
            else:
                
                rs.set_return_status(0)
                rs.set_return_values('Invalid path entered\n')   
                
                
                return rs
    return rs