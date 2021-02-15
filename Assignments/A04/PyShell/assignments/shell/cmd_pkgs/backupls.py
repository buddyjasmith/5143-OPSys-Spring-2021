'''
NAME         top

       ls - list directory contents

SYNOPSIS         top

       ls [OPTION]... [FILE]...

DESCRIPTION         top

       List information about the FILEs (the current directory by
       default).
'''

    
import os
from cmd_pkgs.arg_parser import ArgParse
from cmd_pkgs.return_status import ReturnStatus
from pathlib import Path
import glob
import sys
import stat
from datetime import datetime
from prettytable import PrettyTable
import time
from colorama import Style, Fore
import glob

# Module doc string for error messages
arg_dict = {
    'l': False,
    'a': False,
    'h': False,
}
text_color = {
    'file': '\033[92m',
    'dir': '\033[94m',
    'default:': '\033;[37m',
}
size_dict ={
    'BYTES': 1,
    'KB' : 2,
    'MB' : 3,
    'GB' : 4,
}
def ls( args , cwd):
    '''
    :Function: ls
    :Parameters: args: commands passed from shell.py
    :          : cwd:
    :Usage: ls [-flags] [paths]
    :Returns: ReturnStatus object
    :Description: ls is the call function for the ls method called from shell.py.  If 
    :           : no flags are called, simples_ls1.  If only a path is given, simple_ls1
    :           : is still called and the results are returned to the caller for output.
    :           : For more complex calls involving flags, the complex_ls command is called
    :           : and the results are returned to ls to be returned to shell.py.
    :Problems: None as of yet
    :To-Dos: More functionality. I had to lose some functionality after refactoring
    '''
    #remove command from args
    arg_parse = ArgParse(args, arg_dict, cwd, __doc__)
    flags = arg_parse.get_flags()
    rs = ReturnStatus()
    rs.set_cwd(cwd)
    print(len(args))
    directories = arg_parse.get_directories()
    if not directories:
        directories.append(os.path.abspath(cwd))
    
    if (len(args) == 1 ):
        simple_ls1(flags, directories, rs)
        rs.set_return_status(1)
        
        return rs
    elif(len(args) ==2) and (('a' in flags) or ('h' in flags)) and ('l' not in flags):
        print('Am i entering here')
        simple_ls1(flags, directories,rs)
        return rs
    else:
       
        
        if not flags:
            
            simple_ls1(flags,directories, rs)
            return rs
        elif flags:
            complex_ls(directories,flags,rs)
            
            return rs
    rs.set_return_status(0)
    rs.set_return_values('Mystery problem achieved')

    return cwd
def simple_ls1(flags, paths, rs):
    '''
    :Function: simple_ls1
    :Parameters: flags: user defined flags passed to the method
    :          : paths: path to be listed
    :          : rs: ReturnStatus object to be returned to user 
    :Usage: This method is called 
    :Returns: RS object
    :Description: this function does a directory listing for the paths provided.
    :           : attributes will not be returned via this method
    :Problems: none
    :To-Dos: none
    '''
    sys.stdout.write('\n')
    sys.stdout.flush()
    results = ''
    for path in paths:
        if os.path.isfile(path):
            results += str(path +'\n' )   
        elif os.path.isdir(path):
            for file in os.listdir(path):
                if(file.startswith('.')):
                    if(flags) and (('h' in flags) or ('a' in flags)):
                        results += str(file + '\n')
                    else:
                        continue
                else:
                    results += str(file +'\n')
    rs.set_return_status(1)
    rs.set_return_values(results)
    
    return rs
def convert_unit(size_in_bytes):
    '''
    :Function: convert_unit
    :Parameters: size_in_bytes
    :Usage: not commandline callable
    :Returns: integer 
    :Description: converts bytes to kb
    :Problems: nada
    :To-Dos: none
    '''
    size = size_in_bytes / 1024
    return round(size,2)


def __exe_ls(file_path, flags_list, file_name,rs):
    '''
    :Function: __exe_ls
    :Parameters: file_path: path to check
    :          : flags_list: list of flags parsed
    :          : file_name: name of file to collect attys on
    :Usage: not commandline callable
    :Returns: list 
    :Description: this function is passed a file path, attributes are collected
    :           : on the given file path by default in non human form.  if the 
    :           : -h method is passed.  results are transformed into human readable 
    :           : content
    :Problems: nada
    :To-Dos: none
    '''
    full_path = os.path.join(file_path,file_name)
    dir_results = []
   
    
    _stats = os.stat(full_path)
    _path = Path(full_path)
  
    dir_results = []
    if('l' in flags_list):
        try:
            name = file_name
            color = Fore.BLUE if os.path.isdir(full_path) else Fore.GREEN

            color_name = str(color + name + Style.RESET_ALL)
            file_mode = _stats.st_mode
            nlink = _stats[stat.ST_NLINK]
            owner = _stats.st_uid
            group = _stats.st_gid
            size = _path.stat().st_size
            time = _stats.st_mtime
            if 'h' in flags_list:
                file_mode = stat.filemode(file_mode)
                owner = _path.owner()
                group = _path.group()
                size = convert_unit(size) 
                size = str(f'{size} KB') 
                time = datetime.fromtimestamp(_stats.st_mtime).strftime('%Y-%h-%d %H:%M')
            
            dir_results.append(color_name)
            dir_results.append(file_mode)
            dir_results.append(nlink)
            dir_results.append(owner)
            dir_results.append(group)
            dir_results.append(size)
            dir_results.append(time)
            return_results = [
                name,
                file_mode,
                nlink,
                owner,
                group,
                size, 
                time
            ]
            rs.set_return_status(1)
            
        except Exception:
            sys.stdout.write(Fore.RED + 'Invalid file path' + Style.RESET_ALL)
    
        return dir_results

def complex_ls(paths, flags, rs):
    '''
    :Function: complex_ls
    :Parameters: paths: all paths passed by the user
    :          : flags: flags passed by user
    :          : rs: ReturnStatus object, to collect data and return to shell
    :Usage: not commandline callable
    :Returns: none, changes rs data 
    :Description: iterates through the directories passed by user and calls
    :           : __exe_ls to collect file attributes.  Results are passed back
    :           : via a table format and stored in RS
    :Problems: nada
    :To-Dos: none
    '''
    list_results = []
    sys.stdout.write('\n')
    # dir_results = {}
    table = PrettyTable()
    # if no paths exist, none were given set path to current directory
    ##  This needs to improved, sets cwd to where python file is
    
    if (not paths):
        paths.append(os.getcwd())
    for path in paths:
        if (os.path.isdir(path)):
            for i in os.listdir(path):
                full_path = os.path.join(i, path)
                results = __exe_ls(full_path, flags, i,rs)
                list_results.append(results)
        elif os.path.isfile(path):
            directory_path = os.path.dirname(path) + '/' 
            file_name = path_leaf(path)
            
            results = __exe_ls(directory_path, flags, file_name,rs)
            list_results.append(results)
        elif not os.path.exists(path):
            rs.set_return_status(0)
            rs.set_return_values(str(Fore.RED + 'Invalid path entered \n'))
            rs.set_return_values(str(Fore.RED + __doc__ + '\n'))
            #sys.stdout.write(Fore.RED + 'Invalid path entered \n')
            #sys.stdout.write(Fore.RED + __doc__ + '\n')
            return rs
    table.header = False
    table.border = False
    for list in list_results:
        table.add_row(list)
    table_txt = table.get_string()
    
    rs.set_return_values(table_txt)
    
    return


def path_leaf(path):
    # collects the filename from a path
    return os.path.basename(path)

def get_file_attributes():
    with os.scandir() as dir_entries:
        for entry in dir_entries:
            info = entry.stat()
            
