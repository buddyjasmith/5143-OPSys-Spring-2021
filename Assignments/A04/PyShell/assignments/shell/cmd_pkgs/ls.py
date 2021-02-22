'''
NAME:
       ls - list directory contents
SYNOPSIS:
       ls [OPTION]... [FILE]...
DESCRIPTION:
       List information about the FILEs (the current directory by
       default).
'''
from os.path import basename
from cmd_pkgs.return_status import ReturnStatus
from cmd_pkgs.arg_parser import ArgParse
from prettytable import PrettyTable
from pathlib import Path
import stat
import math
import datetime
from colorama import Fore, Style
import os
import traceback
import prettytable
from datetime import datetime, timezone
arg_dict = {
    'l': 0o100,
    'a': 0o010,
    'h': 0o001,
}
def ls(args, cwd):
    rs = ReturnStatus()
    rs.set_cwd(cwd)
    ap = ArgParse(args, arg_dict, cwd, __doc__)
    flags = ap.get_flags()
    directories = ap.get_directories()
    help_flag = [x for x in args if x.startswith('--help')]
    if help_flag:
        rs.set_return_status(1)
        rs.set_return_values(__doc__)
        return rs
    if 'INVALID PATH' in directories:

        rs.set_return_status(0)
        rs.set_return_values('INVALID PATH')
        return rs
    if len(directories) == 0:
        directories.append(os.path.abspath(cwd))
    
    octal_flag = get_octal_count(flags)
    call_ls_type(octal_flag, directories,rs, cwd)
    return rs

def get_octal_count(flags):
    # 8 possible outcomes exist, but in reality, 4 pairs tr
    base = 0o000
    base |= 0o100 if 'l' in flags else 0o000
    base |= 0o010 if 'a' in flags else 0o000
    base |= 0o001 if 'h' in flags else 0o000
    return base
def call_ls_type(octal_flag, directories, rs, cwd):
    if (octal_flag == 0o0) or (octal_flag == 0o001):
        just_ls(directories, rs,cwd)
    elif (octal_flag == 0o010) or (octal_flag == 0o011):
        all_ls(directories, rs,cwd, octal_flag)
    elif (octal_flag == 0o100 ) or (octal_flag == 0o101):
        long_ls(directories, rs,cwd,octal_flag)
    elif (octal_flag == 0o110) or (octal_flag == 0o111):
        long_ls(directories, rs,cwd,octal_flag)

def just_ls(directories, rs, cwd):
    # Equivalent to ls or ls -h
   
    dir_results = []
    file_results = []
   
    for directory in directories:
        # iterate passed directories
        if os.path.isdir(directory):
            for i in os.listdir(directory):
                # if di
                if os.path.isdir(i):
                    if not i.startswith('.'):
                        dir_results.append(str( i ))
                else:
                    if not i.startswith('.'):
                        file_results.append(str( i ))
        elif os.path.isfile(directory):
            file_results.append(os.path.basename(directory))
    temp=''
    if dir_results:
        dir_results.sort()
        temp += '\n'.join(dir_results)
    temp += '\n'  
    if file_results:
        file_results.sort()
        temp += '\n'.join(file_results)
    if len(temp) > 0:
        rs.set_return_values(temp)
        rs.set_return_status(1)
    else:
        rs.set_return_status(0)
        rs.set_return_values(__doc__)
    return
    
        
        
def all_ls(directories, rs,cwd,octal_flag):
    
    # function is equivalient to ls -a or ls -ah
    hidden_files = []
    hidden_files.append(str( '.\n'))
    hidden_files.append(str('..\n' ))
    rs.set_return_status(1)
    file_results = []
    dir_results = []
   
    for directory in directories:
        # iterate passed directories
        if os.path.isdir(directory):
            for i in os.listdir(directory):
                abspath = os.path.abspath(os.path.join(directory,i))
                # if di
                if os.path.isdir(abspath):
                    if not i.startswith('.'):
                        dir_results.append(str(i + '\n'))
                elif os.path.isfile(abspath):
                    if i.startswith('.'):
                        hidden_files.append(str( i + '\n'))
                    elif not i.startswith('-'):
                        file_results.append(str( i + '\n'))
        elif os.path.isfile(directory):
            basename = os.path.basename(directory)
            if basename.startswith('.'):
                hidden_files.append(basename)
            else:
                file_results.append(basename)
    temp = '\n'
    if dir_results:
        dir_results.sort()
        temp += ''.join(dir_results)
    if file_results:
        file_results.sort()
        temp += ''.join(file_results)
    if hidden_files:
        temp += ''.join(hidden_files)
    
    
    if len(temp) > 0:
        rs.set_return_status(1)
        rs.set_return_values(temp)
    else:
        rs.set_return_status(0)
        rs.set_return_value('Something went wrong')
    return


def long_ls(directories, rs,cwd,octal_flag):
    
    hidden_files = []
    hidden_directories =[]
    reg_files = []
    reg_directories = []
    
    all_flag = octal_flag & 0o010
   
    list_all = (all_flag == 0o010)
    
   
    for directory in directories:
        
        if os.path.isdir(directory) :
            dir_len = len([x for x in os.listdir(directory) if os.path.isdir(x)])
            for i in os.listdir(directory):
                
                abspath = os.path.abspath(os.path.join(directory,i))
               
                # history flag present
                    
                # if di
                if os.path.isdir(abspath):
                    if i.startswith('.') and (list_all == True) and (not '.localized' in i):  
                        hidden_directories.append(__exe_ls(abspath, octal_flag,cwd))
                    else:
                        reg_directories.append(__exe_ls(abspath, octal_flag,cwd))
                elif os.path.isfile(abspath):
                    if i.startswith('.') and (list_all == True):
                        hidden_files.append(__exe_ls(abspath, octal_flag,cwd))
                    elif not 'localized' in abspath and not i.startswith('.'):
                        reg_files.append(__exe_ls(abspath, octal_flag,cwd))
        elif os.path.isfile(directory):
            
            
            if directory.startswith('.'):
                pass
                #hidden_files.append(__exe_ls(basename,directory, octal_flag,cwd))
            else:
                reg_files.append(__exe_ls(directory, octal_flag,cwd))
        else:
            reg_directories.append(__exe_ls(directory, octal_flag,cwd))
    temp = ''
    pt = PrettyTable()
    pt.border = False
    pt.header = False
    if hidden_files and (list_all == True):
        hidden_files.sort()
        for file in hidden_files:
            
            pt.add_row(file)
        
    if reg_files:
        reg_files.sort()
        for file in reg_files:
            
            pt.add_row(file)
        
    if reg_directories:
        reg_directories.sort()
        for file in reg_directories:
           
            pt.add_row(file)
    temp = pt.get_string()  
    
    
    if temp:
        rs.set_return_status(1)
        rs.set_return_values(temp)
    else:
        rs.set_return_status(0)
        rs.set_return_values('Invalid pathb')
     
            
def __exe_ls( directory, octal_flag, cwd):
    
    dir_results = []
    
    try:
        _stats = os.stat(directory)
        _path = Path(directory)
    except NotADirectoryError:
        return[]
  
    dir_results = []
    try:
        attys = _stats.st_mode
        nlink = _stats[stat.ST_NLINK]
        attys = stat.filemode(attys)
        owner = _path.owner()
        group = _path.group()
        size = _path.stat().st_size
        time = datetime.fromtimestamp(_stats.st_mtime).strftime('%Y-%h-%d %H:%M')

        if octal_flag & 0o001 == 0o001: # if human flag convert bytes to 
            size = get_printable_size(size)
        dir_results.append(str(attys))
        dir_results.append(str(nlink))
        dir_results.append(str(owner))
        dir_results.append(str(group))
        dir_results.append(str(size))
        dir_results.append(str(time))
        dir_results.append(str( os.path.basename(directory) ))
    except Exception as ex:
        dir_results.append(f'Something went wrong with {directory}')
        return dir_results
        

       

    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        dir_results.append(str(template))
        dir_results.append(str(message))
    return dir_results

def long_all_ls(directories, rs):
    pass
def get_printable_size(byte_size):
    # I found this online, seemed like a worthwhile solution.  Referrence is included
    """
    A bit is the smallest unit, it's either 0 or 1
    1 byte = 1 octet = 8 bits
    1 kB = 1 kilobyte = 1000 bytes = 10^3 bytes
    1 KiB = 1 kibibyte = 1024 bytes = 2^10 bytes
    1 KB = 1 kibibyte OR kilobyte ~= 1024 bytes ~= 2^10 bytes (it usually means 1024 bytes but sometimes it's 1000... ask the sysadmin ;) )
    1 kb = 1 kilobits = 1000 bits (this notation should not be used, as it is very confusing)
    1 ko = 1 kilooctet = 1000 octets = 1000 bytes = 1 kB
    Also Kb seems to be a mix of KB and kb, again it depends on context.
    In linux, a byte (B) is composed by a sequence of bits (b). One byte has 256 possible values.
    More info : http://www.linfo.org/byte.html
    """
    BASE_SIZE = 1024.00
    MEASURE = ["B", "KB", "MB", "GB", "TB", "PB"]

    def _fix_size(size, size_index):
        if not size:
            return "0"
        elif size_index == 0:
            return str(size)
        else:
            return "{:.3f}".format(size)

    current_size = byte_size
    size_index = 0

    while current_size >= BASE_SIZE and len(MEASURE) != size_index:
        current_size = current_size / BASE_SIZE
        size_index = size_index + 1

    size = _fix_size(current_size, size_index)
    measure = MEASURE[size_index]
    return size + measure