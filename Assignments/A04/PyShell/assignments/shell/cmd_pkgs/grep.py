'''
Name: Grep
SYNOPSIS
       grep [OPTION...] PATTERNS [FILE...]
Flags:  
    -l supress normal output.  Instead, print the name of each input file
       where the matching pattern was found.  
'''
from cmd_pkgs.arg_parser import ArgParse
from cmd_pkgs.return_status import ReturnStatus
import os
import sys
from colorama import Fore, Style
cmd_dict ={
    'l': False
}
flags = []
def grep(args, cwd):
    '''
    :Function:      grep
    :Usage:         grep [flags] [patterns] [File/Directory]
    :Author:        Buddy Smith
    :Parameters:    args: parameters from command line
    :               cwd: current working directory
    :Description:   the function checks for existing patterns in a file. If the -l flag is
    :               passed, only the file name will be printed if found.  If not passed, the line number,
    :               text matching expression will be printed to the screen
    :Todo:          Test more, Add Recursive option?>
    :Returns:       Returns the ReturnStatus object consisting  of status, return values, and the cwd
    :Bugs:          None at this time
    '''
    sys.stdout.write('\n')
    sys.stdout.flush()
    rs = ReturnStatus()
   
    rs.set_cwd(cwd)
    help_flag = [x for x in args if x.startswith('--help')]
    if help_flag:
        rs.set_return_status(1)
        rs.set_return_values(__doc__)
        return rs
    # systematically remove flags and expressions from args to be left with file/directory to search
    args.remove('grep')
    flags = [x for x in args if  x.startswith('-')]    # get list of items that start with '-'
    args = [x for x in args if not x.startswith('-')]  # remove items that start with '-' from args
    regexp = [x for x in args if  x.startswith("'")]   # collect regular expressions from args
    path = [x for x in args if not x.startswith("'")]
    
    exp = str(regexp[0])
    # print(str(exp[1:-1]))
    exp_list = []
    for i in regexp:
        temp = i[1:-1] #remove quotes from expression
        exp_list.append(temp)

    
    
    
    # print(f'\npaths={path}')
    # print(f'regexp={regexp}')
    # print(f'flags={flags}')
    
    # determine if path exists, if not path is cwd, get abspath of either instance
    temp=[]
    if path:
        for i in path:
            temp.append( os.path.abspath(os.path.join(cwd,i)))
    else: 
        temp.append(os.path.abspath(os.path.joiin(cwd,i))    )
    path = temp
    # print(path)
    
    return_set = set()
    return_dict = {}
    for p in path:
        
        found = ''
        
        if os.path.isfile(p):
            
            return_dict[p] = set()
            line_number = 0
            try:
                with open(p, 'r') as read_obj:
                    for line in read_obj:
                        line_number +=1
                        for exp in exp_list:
                            if exp in line:
                                if '-l' in flags:
                                    rs.set_return_status(1)
                                    found = str(f'{os.path.basename(p)}')
                                    return_set.add(found)
                                else:
                                    rs.set_return_status(1)
                                    temp = line.strip()
                                    found = str(f'File: {os.path.basename(p)}\t0{str(line_number)}\t {temp}\n')
                                    return_set.add(found)
            except Exception:
                rs.set_return_values('Unable to open file')
                rs.set_return_status(0)
                return rs
                            #temp = line.lstrip()
                            #results[line_number] = temp
                            #sys.stdout.write(f'{str(line_number)}\t  {temp}')
                            #sys.stdout.flush()
                        
        elif os.path.isdir(p):
            rs.set_return_values(str(Fore.YELLOW + f'grep: {p}: Is a directory\n' +Style.RESET_ALL))
            
        elif not os.path.exists(p):
            rs.set_return_values(str(Fore.RED + 'Invalid path given\n' + Style.RESET_ALL))
            
        else:
            rs.set_return_values(str(Fore.RED + 'Internal Error: Something went wrong\n' + Style.RESET_ALL))
            
    if return_set :
        item = list(return_set)
        item = sorted(item)
        temp = ''.join(item)
        rs.set_return_values(temp)
        
        
    
        
    return rs
 