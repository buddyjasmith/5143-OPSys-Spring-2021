import sys
import os
from colorama import Fore, Style
class ArgParse:
    '''
    : Class         : Argparse
    : Contructor    : Parameterized
    : Parameters    : *args passed from the user, aka shell commands
    : Methods       : parse_args()
    :               : get_flags(commands_dict)
    :               : get_paths()
    :               : _valid_or_not()
    : Data          : args[], flags[], file_paths[]
    : Description   : ArgParse is initiliazed via arguments passed via pyshell.  Arguments are split and stored into
    :               : class data members, for retrieval and verification before usage.
    '''
    def __init__(self, cmd_in, cmd_dict, cwd, doc):
        self.int_flags = 0
        self.flags = []
        self.directories = []
        self.cmd_in = cmd_in
        self.cmd_dict = cmd_dict
        self.cwd = cwd
        self.asn_operators =[]
        self.operands = ['+', '-', '=']
        self.misc_parameters = []
        self.caller_doc = doc
        self.parse_args()
        
    def __check_equals(self, args):
        
        for iter0 in args:
            for iter1 in self.operands:
                if iter1 in iter0:
                    self.asn_operators.append(iter0)
        args = [iarg for iarg in args if not any(xop in iarg for xop in self.asn_operators)]
       
        
    def parse_flags(self, args):
        
        if args.startswith('--'):
            potential_flag = args[2:]
            if potential_flag in self.cmd_dict:
                self.flags.append(potential_flag)
            
        else:
            potential_flags = args[1:]
            potential_flags = list(potential_flags)
            for x in potential_flags:
                if x in self.cmd_dict:
                    self.flags.append(x)
           
    def get_int_flags(self, args):
        if self.cmd_in[1:]:
            args = self.cmd_in[1:]
         
            for item in args:
                if item.startswith('-'):
                    potential_n = item[1:]
                   
                    if isinstance(int(potential_n), int):
                        self.int_flags = int(potential_n)
                        return self.int_flags
    
               

       
    def parse_args(self):
        os.chdir(self.cwd)
        
        if self.cmd_in[1:]:
            args = self.cmd_in[1:]
            
            self.__check_equals(args)
            for item in args:
                
                if item == '~':
                    path = os.path.expanduser(item)
                    self.directories.append(path)
                elif( item.startswith('--') or item.startswith('-')):
                    self.parse_flags(item)
                else:
                    abs_path = os.path.abspath(item)
                    
                    if(os.path.exists(abs_path)):
                        self.directories.append(abs_path)
                    elif '*' in abs_path:
                        wild_path = os.path.join(self.cwd,abs_path)
                        self.directories.append(wild_path)
                    else:
                        self.directories.append('INVALID PATH')
                        return

    def get_flags(self):
        return self.flags
    def get_directories(self):
        return self.directories
   