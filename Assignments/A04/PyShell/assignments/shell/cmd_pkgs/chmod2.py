'''
Name: chmod
Modifiers:           r: read
                     w: write
                     x: execute
Octal Modifier:      Octals can be used as a modifier:
                     example: 100 : all user rights given
                              010 : all group rights given
                              001 : other rights given
                              777 : all rights to eveyone DANGER!
                     
chmod u+r filename   u means the file owner
chmod u+w filename   adds write right
chmod u+x filename   add execute right

chmod g+r filename   g means the user who are member of the group
chmod g+w filename
chmod g+x filename

chmod o+r filename   o means all others
chmod o+w filename
chmod o+x filename
Description:    Change user, group, and other access rights to files/folders

'''
#chmod u+r filename   u means the file owner
#chmod u+w filename
#chmod u+x filename

#chmod g+r filename   g means the user who are member of the group
#chmod g+w filename
#chmod g+x filename

#chmod o+r filename   o means all other users
#chmod o+w filename
#chmod o+x filename

import os

import stat
import sys
from .return_status import ReturnStatus
from colorama import Fore, Style

from cmd_pkgs.arg_parser import ArgParse
from cmd_pkgs.return_status import ReturnStatus
def chmod2(args, cwd):
    rs = ReturnStatus()
    rs.set_cwd(cwd)
    help_flags = [x for x in args if x.startswith('--help')]
    if help_flags:
        rs.set_return_status(1)
        rs.set_return_values(Fore.YELLOW + str(__doc__) + Style.RESET_ALL)
        return rs
    octal_values = None
    paths = None
    modifys = None
    args.pop(0)
    
    
    first_value = args[0]
    path = args[1]
    
   
    try:
        octal_values = int(first_value,8)
        
    except Exception:
        modifys = first_value
    
    
    
    if isinstance(octal_values,int):
        
        simple_ch_mod(octal_values, path,cwd, rs)
        return rs

    if path and modifys:
       
        abs_path = os.path.abspath(os.path.join(cwd,path))
        
        if not os.path.exists(abs_path):
            rs.set_return_status(0)
            rs.set_return_values(Fore.RED + 'Invalid path given.' + Style.RESET_ALL)
            rs.set_return_values(__doc__)
            return rs
    else:
        rs.set_return_status(0)
        rs.set_return_values(__doc__)
        return rs
    if not modifys == None:
        current = stat.S_IMODE(os.lstat(abs_path).st_mode) # get the current value represented in oct 
        # create octal number for every option u g and o 
        u_bit_piece = 0o000
        g_bit_piece = 0o000
        o_bit_piece = 0o000
        
        if 'x' in modifys:
            u_bit_piece = u_bit_piece | 0o100
            g_bit_piece = g_bit_piece | 0o010
            o_bit_piece = o_bit_piece | 0o001
        if 'w' in modifys:
            u_bit_piece = u_bit_piece | 0o200  
            g_bit_piece = g_bit_piece | 0o020  
            o_bit_piece = o_bit_piece | 0o002         
        if 'r' in modifys:
            u_bit_piece = u_bit_piece | 0o400
            g_bit_piece = g_bit_piece | 0o040
            o_bit_piece = o_bit_piece | 0o004
        total_bit_piece = 0o000
        if 'g' in modifys:
            total_bit_piece |= g_bit_piece
        if 'o' in modifys:
            total_bit_piece |= o_bit_piece
        if 'u' in modifys:
            total_bit_piece |= u_bit_piece
        if '+' in modifys:
            os.chmod(abs_path, current | total_bit_piece)
        elif '-' in modifys:
            os.chmod(abs_path, current ^ total_bit_piece)
        elif '=' in modifys:
            os.chmod(abs_path, o_bit_piece)
        
        previous = current
        current = stat.S_IMODE(os.lstat(abs_path).st_mode)
        if not current == previous:
            
            rs.set_return_status(1)
            rs.set_return_values(abs_path)
            return rs
    else:
       
         num = str(''.join(octal_values)) 
         os.chmod(abs_path, int(num, 8) )
         rs.set_return_status(1)
         rs.set_return_values(abs_path)
         # file permissions were changed.
         
    return rs
def simple_ch_mod(octal_values, path,cwd, rs):
    
    abs_path = os.path.abspath(os.path.join(cwd,path))
    previous = stat.S_IMODE(os.lstat(abs_path).st_mode)
    
    os.chmod(abs_path, octal_values )
    current = stat.S_IMODE(os.lstat(abs_path).st_mode)
    
    rs.set_return_status(1)
    rs.set_return_values(abs_path)
         # file permissions were changed.
