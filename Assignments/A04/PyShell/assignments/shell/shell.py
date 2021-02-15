
import traceback
import os
import concurrent.futures as cf
import sys, tty
from time import sleep
from readchar import readchar, readkey
from itertools import cycle
from cmd_pkgs.ls import ls
from colorama import Fore, Style

from cmd_pkgs.banner import print_banner
from cmd_pkgs.banner import print_banner
from cmd_pkgs.cd import cd
from cmd_pkgs.chain_helper import ChainHelper
from cmd_pkgs.touch import touch
from cmd_pkgs.rm import rm
from cmd_pkgs.mv import mv
from cmd_pkgs.head import head
from cmd_pkgs.chmod2 import chmod2
from cmd_pkgs.mkdir import mkdir 
from cmd_pkgs.history import history, get_history, set_history
from cmd_pkgs.return_status import ReturnStatus
from cmd_pkgs.pwd import pwd
from cmd_pkgs.rmdir import rmdir
from cmd_pkgs.grep import grep
from cmd_pkgs.cp import cp
from cmd_pkgs.sort import sort
from cmd_pkgs.file_redirect import file_redirect, file_append
from cmd_pkgs.tail import tail
from cmd_pkgs.wc import wc
from cmd_pkgs.cat import cat
from cmd_pkgs.who import who
from cmd_pkgs.help import help
command_dict = {
        'ls': ls,
        'cat': cat,
        'cd': cd,
        'mv': mv,
        'rm': rm,
        'head': head,
        'help': help,      
        'mkdir' : mkdir,
        'grep' : grep,
        'pwd' : pwd,
        'rmdir' : rmdir,
        'cp' : cp,
        'tail': tail,
        'history': history,
        'tail': tail,
        'chmod': chmod2,
        'sort': sort,
        '>' : file_redirect,
        '>>' : file_append,
        'wc' : wc,
        'who' : who,
        'ls': ls,
        'touch' : touch
        
}




def print_cmd( cmd):
   
    prompt = str(f'%:' )
    padding = " " * 80
    sys.stdout.write(Fore.CYAN + Style.BRIGHT+ "\r" + padding)
    sys.stdout.write("\r"+ prompt + Style.RESET_ALL+ cmd)
    sys.stdout.flush()
class Shell:
    
    def __init__(self):
        self.cwd = os.path.expanduser('~')
        self.hist_list = get_history()
        print_banner()
        self.main()
        
        colorama.init()
    

    def main(self):
        
        start_ptr = 0
        hist_ptr = len(self.hist_list) -1
        cmd = ''
        print_cmd(cmd)
        while True:
            char = readchar()
            if char == '\x03' or cmd == 'exit': # ctrl-c
                set_history(self.hist_list)
                raise SystemExit("Bye.")
            elif char in ('\b', 'KEY_BACKSPACE', '\x7f'):
                cmd = cmd[:-1]
                
                    
                print_cmd(cmd)
            elif char in '\r':
                if cmd.startswith('!'):
                    temp = int(cmd[1:])
                    cmd = self.hist_list[temp-1]
               
                self.hist_list.append(cmd)
                cmd = cmd.split()
                hist_ptr = len(self.hist_list) -1
                ch = ChainHelper(cmd)
                ch_cmds = ch.get_chain_cmds()
                
                ch_order = ch.get_chain_order()
                
                self.execute_commands(ch_cmds, ch_order)
                cmd = ''
                print_cmd(cmd)
   
            elif char in '\x1b':
                null = readchar()
                direction = readchar()
                if direction in 'A':  
                    hist_ptr -= 1 
                    cmd = self.hist_list[hist_ptr % len(self.hist_list)] 
                    
                    print_cmd(cmd)
                elif direction in 'B':
                    hist_ptr += 1
                    cmd = self.hist_list[hist_ptr  % len(self.hist_list)]
                    
                    print_cmd(cmd) 
                
                    
                # elif direction in 'D':            # right arrow pressed
                #     # moves the cursor to the RIGHT on your command prompt line
                #     # prints out '→' then erases it (just to show something)
                #     cmd += '→'
                #     print_cmd(cmd)
                #     sleep(0.3)
                #     cmd = cmd[:-1]
            else:
                
                cmd = cmd +char                     # add typed character to our "cmd"
                print_cmd(cmd)                  # print the cmd out

    def calculate_carryover(self,ch_cmds, ch_order,carry_over,arg):
        if carry_over:
                # if value is found in carry_over, extend second argument with contents of carry_over
                if not ch_order[0] == '|':
                    
                    arg.extend(carry_over)
                    carry_over = []
                    arg.insert(0, ch_order[0])
                    ch_order.pop(0)
                else:
                    
                    arg.extend(carry_over)
                    carry_over = []
                   
                    ch_order.pop(0) 

    def execute_commands(self,ch_cmds, ch_order):
        sys.stdout.write('\n')
        sys.stdout.flush()
        carry_over = []
       
        redirect_flag = False
        for arg in ch_cmds:
        
            
            if carry_over:
                self.calculate_carryover(ch_cmds,ch_order,carry_over,arg)

                # if value is found in carry_over, extend second argument with contents of carry_over
                # if not ch_order[0] == '|':
                    
                #     arg.extend(carry_over)
                #     carry_over = []
                #     arg.insert(0, ch_order[0])
                #     ch_order.pop(0)
                # else:
                    
                #     arg.extend(carry_over)
                #     carry_over = []
                   
                #     ch_order.pop(0)
                
            try:
               
                with cf.ThreadPoolExecutor() as executor:
                    thread = executor.submit(
                        command_dict.get(arg[0]), arg, self.cwd
                    )
                rs = thread.result()
                
            except TypeError as ex:
                sys.stdout.write('\nInvalid PyShell Command given\n')
                sys.stdout.flush()
                # template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                # message = template.format(type(ex).__name__, ex.args)
                
                # print (message)
                # print(traceback.format_exc())
                return
            except FileNotFoundError:
                sys.stdout.write('Invalid File path given')
            self.cwd = rs.get_cwd() # store current directory returned from functions
            
            return_value = rs.get_return_values() # get return values
            status = rs.get_return_status() # status will be 1 = True, or False = 0
           
            if ch_order :
                 
                # if chain was passed, checked after first argument execution to get the first value in the list
                first_chain = ch_order[0]
                
                if status == 1:
                    # chain exists and previous execution returned status 1
                    keep_loop = self.ch_true_stat_1(ch_order,return_value,carry_over)
                    if keep_loop == True:
                        continue
                    else:
                        break
                    #Chain exists and status is 1
                    # if first_chain == '||':
                    #     # first command was executed successfully, break, dont do 2nd comman
                    #     return
                    # elif first_chain == '|':
                    #     return_value = return_value.splitlines()
                    #     carry_over.extend(return_value)

                    # elif first_chain == '&&':
                       
                    #     sys.stdout.write('\n')
                    #     ch_order.pop(0)
                    #     continue
                    # elif first_chain == '>':
                    #     return_value= ' ' + return_value
                    #     carry_over.extend(return_value)
                    #     redirect_flag = True
                    # elif first_chain == '>>':
                    #     carry_over.extend(return_value)
                    #     redirect_flag = True
                elif status == 0:
                    # chain operator exists but returned status 0 from first execution
                    keep_loop = self.ch_true_stat_0(ch_order,return_value,carry_over)
                    if keep_loop == True:
                        continue
                    else:
                        break
                    # if first_chain ==  '&&':
                    #     ch_order.pop(0)
                    #     sys.stdout.write(Fore.RED + f'\nFirst Command Failed:\n' + Style.RESET_ALL)
                    #     sys.stdout.write(Fore.YELLOW + f'\t:{return_value}' + Style.RESET_ALL)
                    #     sys.stdout.flush()
                    #     return
                    # elif first_chain == '||':
                    #     sys.stdout.write(Fore.RED + f'\nFirst Command Failed:\n' + Style.RESET_ALL)
                    #     sys.stdout.write(Fore.YELLOW + f'\t:{return_value}' + Style.RESET_ALL) 
                    #     sys.stdout.flush()
                    #     ch_order.pop(0)
                    # elif first_chain == '>':
                    #     sys.stdout.write(Fore.RED + f'\nFirst Command Failed:\n' + Style.RESET_ALL)
                    #     sys.stdout.write(Fore.YELLOW + f'\t:{return_value}' + Style.RESET_ALL)
                    #     sys.stdout.flush()
                    #     return

            elif status == 1:
                # no chain was detected, just print the return values
                sys.stdout.write(str('\n' + return_value + '\n'))
                sys.stdout.flush()
                #print('\n'+return_value)
                continue
            elif status == 0:
                
                #No chain was detected, command failed.  Return failure
                # No matter what I try, I can not get sys.stdout.write to work here...
                # I am having use a print statement against standards for the project
               
                # sys.stdout.write('\n')
                # sys.stdout.flush()
                # sys.stdout.write(str(Fore.RED + return_value + Style.RESET_ALL))
                # sys.stdout.flush()
                print(str(Fore.RED + return_value + Style.RESET_ALL))
                return
    def ch_true_stat_1(self, ch_order, return_value, carry_over):
        first_chain = ch_order[0]
        if first_chain == '||':
            sys.stdout.write(str(return_value)) 
            sys.stdout.flush()
            return False
        elif first_chain == '|':
            return_value = return_value.splitlines()
            carry_over.extend(return_value)
            return True
        elif first_chain == '&&':
            sys.stdout.write('\n')
            sys.stdout.write(str(return_value))
            sys.stdout.flush()
            ch_order.pop(0)
            return True
        elif first_chain == '>':
            return_value= ' ' + return_value
            carry_over.extend(return_value)
            redirect_flag = True
            return True
        elif first_chain == '>>':
            carry_over.extend(return_value)
            redirect_flag = True
            return True
    def ch_true_stat_0(self,ch_order,return_value,carry_over):
        first_chain = ch_order[0]
        if first_chain ==  '&&':
            ch_order.pop(0)
            sys.stdout.write(Fore.RED + f'\nFirst Command Failed:\n' + Style.RESET_ALL)
            sys.stdout.write(Fore.YELLOW + f'\t:{return_value}' + Style.RESET_ALL)
            sys.stdout.flush()
            return False
        elif first_chain == '||':
            sys.stdout.write(Fore.RED + f'\nFirst Command Failed:\n' + Style.RESET_ALL)
            sys.stdout.write(Fore.YELLOW + f'\t:{return_value}' + Style.RESET_ALL) 
            sys.stdout.flush()
            ch_order.pop(0)
            return True
        elif first_chain == '>':
            sys.stdout.write(Fore.RED + f'\nFirst Command Failed:\n' + Style.RESET_ALL)
            sys.stdout.write(Fore.YELLOW + f'\t:{return_value}' + Style.RESET_ALL)
            sys.stdout.flush()
            return False      

if __name__=='__main__':

    os.system('cls' if os.name == 'nt' else 'clear')
    
    shell = Shell()