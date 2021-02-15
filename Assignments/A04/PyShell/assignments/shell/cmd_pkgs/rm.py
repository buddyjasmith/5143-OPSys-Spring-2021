'''
rm [OPTION]... FILE... 
This manual page documents the GNU version of rm. rm removes each specified file. By default, it does not remove directories. 

-f, 
    ignore nonexistent files, never prompt 
-r,
    remove directories and their contents recursively 
'''
import sys
import traceback
from cmd_pkgs.arg_parser import ArgParse
from .return_status import ReturnStatus
from pathlib import Path
from colorama import Fore, Style
import glob
import shutil
import os
arg_dict = {
    'r' : False,
    'f': False,
    'y': False
}
def rm(args, cwd):
    '''
    :Function: rm
    :Parameters: args: arguments passed from shell
    :          : cwd: current shell directory
    :Usage: rm [flags] [path]
    :Returns: ReturnStatus object
    :Description: Method will delete the given path parsed by shell if a file or 
    :           : empty directory.  If a non empty directory is parsed, the -r or -f
    :           : flags must be passed or will return a failure status
    :Problems: None
    :To-Dos: none
    '''
    arg_parse = ArgParse(args, arg_dict, cwd, __doc__)
    flags = arg_parse.get_flags()
    directories = arg_parse.get_directories()
    rs = ReturnStatus()
    rs.set_cwd(cwd)
    
    if 'help' in arg_dict:
        sys.stdout.write(__doc__ + '\n')
        rs.set_return_status(1)
        rs.set_return_values(__doc__)
        return rs
    if directories:
        if not flags:
            if directories:
                try:
                    for dir in directories:
                        
                        test = os.listdir(dir)
                        len_test = len(test)
                       
                        if os.path.isdir(dir) and (len_test > 0):
                            raise IsADirectoryError
                        shutil.rmtree(dir)
                        #p = Path(dir)
                        #p.unlink(False)
                        rs.set_return_status(1)
                        rs.set_return_values(dir)
                except FileNotFoundError:
                    rs.set_return_status(0)
                    rs.set_return_values(str(Fore.RED + 'File not found' + Style.RESET_ALL))
                   
                except IsADirectoryError:
                    
                    rs.set_return_status(0)
                    rs.set_return_values(str(Fore.RED +'Directory is not empty\nuse -r to recursively remove directory or -rf to force removal\n'+ Style.RESET_ALL))
                except Exception as ex:
                    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    rs.set_return_status(0)
                    rs.set_return_values(message)
                    rs.set_return_values(traceback.format_exc())
                finally:
                    return rs
            else:
                error = 'rm: missing operand\n'
                error +='use --help for more info\n'
                
                rs.set_return_status(0)
                rs.set_return_values(error)
                return rs
        else:
            # wild card found use glob to collect matching files
            if not any("*" in s for s in directories):
                if 'r' in flags or 'f' in flags:
                    for dir in directories:
                        if os.path.isfile(dir):
                            try:
                                p = Path(dir)
                                p.unlink()
                                
                                rs.set_return_status(1)
                                rs.set_return_values(p)
                            except FileNotFoundError:
                                rs.set_return_status(0)
                                rs.set_return_values(dir + ' :Error parsing file path.')
                                
                            except IsADirectoryError:
                                rs.set_return_status(0)
                                rs.set_return_values(dir +' :Internal Error. Use -r option to delete')
                                

                        elif os.path.isdir(dir):
                            shutil.rmtree(dir)
                            rs.set_return_status(1)
                            rs.set_return_values(dir)

            elif any("*" in s for s in directories):
                wild_paths = [s for s in directories if '*' in s]
                rs.set_return_status(1)
                for wp in wild_paths:
                    for file in glob.glob(wp):
                        sys.stdout.write(file + '\n')
                        command = input(Fore.RED + "Proceed with deletion? (Y)es or (N)o:  " + Style.RESET_ALL)
                        if 'y' in command.lower():
                            rs.set_return_status(1)
                            if os.path.isdir(file):
                               shutil.rmtree(file)
                               
                               rs.set_return_values(file)
                            elif os.path.isfile(file):
                                #print('Filepath is a file')
                                os.remove(file)
                                rs.set_return_values(file)
                        elif 'n' in command.lower():
                            rs.set_return_values(dir + ': user pressed n')
                            continue
                        else:
                            rs.set_return_status(0)
                            rs.set_return_values(dir + ': Invalid choice entered in wildcard deletion prompt')
                            sys.stdout.write('Invalid choice entered\n')


                
           
            return rs
        return rs


                

    
