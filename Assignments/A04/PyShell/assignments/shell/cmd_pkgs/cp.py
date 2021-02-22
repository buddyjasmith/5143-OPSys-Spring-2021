'''
Name: 
    cp
Usage:
    cp [source] [destination]
Description:
    copies one file/folder to a new destination
'''
import os
from cmd_pkgs.return_status import ReturnStatus
from cmd_pkgs.arg_parser import ArgParse
import shutil
import sys
import traceback

def cp(args,cwd):
    '''
    :Function:      cp
    :Usage:         cp [src] [destination]
    :Author:        Buddy Smith
    :Parameters:    args: parameters from command line
    :               cwd: current working directory
    :Description:   the function takes a file path and copies the contents of file path into a destination path. 
    :               A new 'non-existent' file name must be included in the destination
    :Todo:          Implement the -R flag to copy full directories
    :Returns:       Returns the ReturnStatus object consisting  of status, return values, and the cwd
    '''
    rs = ReturnStatus()
    rs.set_cwd(cwd)
    retun_val = ''
    help_flag = [x for x in args if x.startswith('--help')]
    if help_flag:
        rs.set_return_status(1)
        rs.set_return_values(__doc__)
        return rs
    if len(args) == 3:
        
        os.chdir(cwd)
        src = args[1]
        dest = args[2]

        # Get absolute path of files
        src = os.path.abspath(src)
        dest = os.path.abspath(dest)
        src_exists = os.path.exists(src)                
        dest_exists = os.path.exists(dest)
        dest_dir_path = os.path.dirname(dest)
        if src_exists:
            if  dest_exists == False:
            
                try:
                    if not os.path.exists(dest_dir_path):
                        rs.set_return_status(0)
                        rs.set_return_values(f'cp: {dest_dir_path}: Invalid destination')
                        return rs
                    shutil.copyfile(src, dest)
                    rs.set_return_status(1)
                    retun_val += dest
                except Exception as ex:
                    rs.set_return_status(0)
                    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    return_val  = str(message)

            elif dest_exists:
                #sys.stdout.write('Error: Destination file/dir exists in')
                #sys.stdout.flush()
                rs.set_return_status(0)
                retun_val = 'Error: Destination file/dir exists in'
    else:
       
        rs.set_return_status(0)
        retun_val += 'Invalid number of arguments entered\n'
        return_val += str(__doc__)
        
           

    rs.set_return_values(retun_val)
    return rs