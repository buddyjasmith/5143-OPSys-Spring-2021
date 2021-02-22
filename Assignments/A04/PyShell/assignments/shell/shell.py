'''
 Program:       A04 - Python Terminal
 Author:        Buddy Smith / Leila Kalantari
 Main Class:    Shell
 Date:          February 17, 2021
 Contructor:    Default
 Parameters:    None
 Data Members:  cwd: current working directory of the shell, updated with every
                     function call.
                hist_list: a list that stores all contents from the file 
                     history.py.
 Methods:       main() : starting point of shell object, called in the constructor
                calculate_carryover(ch_cmds, ch_order,carry_over,arg) : decides to 
                     pass values from previous function calls, amends args with
                     new information if so
                execute_commands(self,ch_cmds, ch_order): method for calling functions
                     passed by user
                call_here: calls the << here operator, seperate execution method
                ch_true_stat_1(self, ch_order, return_value, carry_over): deals with specific
                     return types from function calls
                ch_true_stat_0: deals with specifc return type from function calls
 Description:   Shell begins being created with a default constructor. An infinite loops is
                created in which each character read is either appended to the cmd string, 
                sends an exit status, calls history, or executes a command.  Caller functions
                are required to send a ReturnStatus() object back with the results and status
                of each function call. Depending on whether chain operators are present 
                in the command, the return status is dealt with in other method calls and 
                values are printed to the screen, or appended to further function calls.

'''
import traceback
import os
import concurrent.futures as cf
import sys, tty
from time import sleep
from readchar import readchar, readkey
from itertools import cycle
from cmd_pkgs.ls import ls
from colorama import Fore, Style
from cmd_pkgs.here import here
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
        'here': here,    
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
    '''
    :Function:      print_cmd
    :Parameters:    cmd: the value of the string cmd residing in the while loop
    :Author:        Dr. Griffin/Buddy Smith/Leila Kalantari
    :Bugs:          Sometimes if created within VS Codes, shell, print out 
    :               is completely off.  Better to use a non simulated terminal
    :               such as xterm or iterm, etc...

    '''
    prompt = str(f'%:' )
    padding = " " * 80
    sys.stdout.write(Fore.CYAN + Style.BRIGHT+ "\r" + padding)
    sys.stdout.write("\r"+ prompt + Style.RESET_ALL+ cmd)
    sys.stdout.flush()
class Shell:
    '''
    Main Class:    Shell
    Date:          February 17, 2021
    Contructor:    Default
    Parameters:    None
    Data Members:  cwd: current working directory of the shell, updated with every
                        function call.
                    hist_list: a list that stores all contents from the file 
                        history.py.
    Methods:       main() : starting point of shell object, called in the constructor
                    calculate_carryover(ch_cmds, ch_order,carry_over,arg) : decides to 
                        pass values from previous function calls, amends args with
                        new information if so
                    execute_commands(self,ch_cmds, ch_order): method for calling functions
                        passed by user
                    call_here: calls the << here operator, seperate execution method
                    ch_true_stat_1(self, ch_order, return_value, carry_over): deals with specific
                        return types from function calls
                    ch_true_stat_0: deals with specifc return type from function calls
    Description:   Shell begins being created with a default constructor. An infinite loops is
                    created in which each character read is either appended to the cmd string, 
                    sends an exit status, calls history, or executes a command.  Caller functions
                    are required to send a ReturnStatus() object back with the results and status
                    of each function call. Depending on whether chain operators are present 
                    in the command, the return status is dealt with in other method calls and 
                    values are printed to the screen, or appended to further function calls.

    '''
    def __init__(self):
        self.cwd = os.path.expanduser('~')
        self.hist_list = get_history()
        
        print_banner()

        self.main()
        
        
    

    def main(self):
        '''
        :Method:        main()
        :Params:        none
        :Returns:       none
        :Description:   main creates a permanant loops until exit or ctrl-c is type in the terminal
        :               each characters is evaluated and either appended to the cmd string, kills the 
        :               terminal, or executes the command given by the user.  The up and down arrow
        :               keys print to stdout a pointer to last or first element of the history list.
        :               main calls the class ChainHelper, arguments are split based upon the existence
        :               of operators present in the command such as | || && < << > >> etc. These results
        :               are then passed to the function execute_commands where commands are executed.
        '''
        start_ptr = 0
        hist_ptr = len(self.hist_list) -1
        cmd = ''
        print_cmd(cmd)
        while True:
            char = readchar()
            if char == '\x03' or cmd == 'exit': 
                # ctrl-c.. Exit the shell program
                set_history(self.hist_list)
                raise SystemExit("Bye.")
            elif char in ('\b', 'KEY_BACKSPACE', '\x7f'):
                # remove last item of cmd
                cmd = cmd[:-1]   
                print_cmd(cmd)
            elif char in '\r':
                # User pressed enter
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
                # Default else: add typed character to our "cmd" and print cmd out
                cmd = cmd +char                     
                print_cmd(cmd)                 

    def calculate_carryover(self, ch_order,carry_over,arg):
        '''
        :Method:        calculate_carryover
        :Params:        ch_order: list containing chain operators in the command
        :               carry_over: value to be appended to new arg b4 execution
        :               arg: argument soon to be executed within main.
        :Description:   calculate carry_over determines if the next arguments
        :               passed by the user should be ammended if the | operator is detected
        :               if not, contents of carry_over are set to an empty list and the operator 
        :               is popped from the list
        '''
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
        '''
        :Method:        execute_commands
        :Params:        ch_cmds: list of commands user wishes executed
        :               ch_order: chain operators passed by user
        :Descriptions:  this functions is passed a list the user wishes to 
        :               have executed, this is cm_cmds.  ch_cmds is a list 
        :               which holds the chain operators passed by the user
        :               after successful execution of an arguments, the first
        :               element of ch_order is checked to see if it has a operator
        :               present in the list, if so, it begins comparissons based on 
        :               the status and values returned from the object, and which chains
        :               are preseent. I
        '''
        sys.stdout.write('\n')
        sys.stdout.flush()
        carry_over = []
       
        redirect_flag = False
        for arg in ch_cmds:
            if ch_order and ch_order[0] == '<<' and ch_cmds and ch_cmds[1]:
                # if chain operator exists in argument and is the here operator,
                # skip the first command in the argument, move to here command and execute
                carry_on = self.call_here(arg,ch_cmds, ch_order, self.cwd)
                if carry_on == False:
                    break


            if carry_over:
                self.calculate_carryover(ch_order,carry_over,arg)
            try:
                with cf.ThreadPoolExecutor() as executor:
                    thread = executor.submit(
                        command_dict.get(arg[0]), arg, self.cwd
                    )
                rs = thread.result()
                
                
            except TypeError as ex:
                
                sys.stdout.write('\nInvalid PyShell Command given\n')
                sys.stdout.flush()
                ##*****************************************************************
                #Uncomment for testing
                # template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                # message = template.format(type(ex).__name__, ex.args)
                # print (message)
                # print(traceback.format_exc())
                return
            except FileNotFoundError:
                sys.stdout.write('Invalid File path given')
            # store current directory returned from functions
            self.cwd = rs.get_cwd() 
            # get return values
            return_value = rs.get_return_values() 
            # status will be 1 = True, or False = 0
            status = rs.get_return_status() 
            if ch_order :
                # chain exists in commands, get value for future ref
                first_chain = ch_order[0]
                if status == 1:
                    # chain exists and previous execution returned status 1
                    keep_loop = self.ch_true_stat_1(ch_order,return_value,carry_over)
                    if keep_loop == True:
                        continue
                    else:
                        break
                elif status == 0:
                    
                    # chain operator exists but returned status 0 from first execution
                    keep_loop = self.ch_true_stat_0(ch_order,return_value,carry_over)
                    if keep_loop == True:
                        continue
                    else:
                        break
                  

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
                
                print(str(Fore.RED + return_value + Style.RESET_ALL))
                return
    def call_here(self,arg,ch_cmds, ch_order, cwd):
        '''
        :Method:      call_here
        :Params:      arg : argument passed by user
        :             ch_cmds: all arguments passed by user
        :             ch_order: list containing the order of chain commmands issued 
        :             by uthe user. 
        :             cwd: current working directory
        :Description: This method calls a specific function, the here operator.
        :             depending on the status of the completion, the contents of the 
        :             returnstatus object passes the values returned from the here
        :             function back to shell, and if true, appends the result to carry_over
        :             for usage in the next function.
        :Returns:     True: continue loops
        :             False: break loops, here was unsuccessful
        :            
        '''
        with cf.ThreadPoolExecutor() as executor:
            thread = executor.submit(
                command_dict.get('here'), ch_cmds[1], self.cwd)
        here_rs = thread.result()
        
        if here_rs.get_return_status() == 1:
            arg.append(here_rs.get_return_values())
            ch_cmds.pop(1)
            ch_order.pop(0)
            return True
        else:
            message = here_rs.get_return_values()
            sys.stdout.write('Here operator failed:\n')
            sys.stdout.write(str(message))
            return False
    def ch_true_stat_1(self, ch_order, return_value, carry_over):
        '''
        :Method:        ch_true_stat_1
        :Params:        ch_order: list
        :               return_value: ReturnStatus() values
        :               carry_over: string
        :Desc:          Represents state of chain detected, returnstatus value of 1
        :               depending on the value of the chain detected, future logic 
        :               is necessitated in order to break from the loops, or append a
        :               carry over value for the next chain command. Returning True
        :               tells the call loop to continue and the carryover has been appended
        :               , False means break from loop,
        :               first command failed
        '''
        first_chain = ch_order[0]
        if first_chain == '||':
            sys.stdout.write(str(return_value)) 
            sys.stdout.flush()
            return False
        elif first_chain == '|' :
            
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
        if first_chain ==  '&&' or first_chain == '|' or first_chain == '>':
            sys.stdout.write(return_value)
            ch_order.pop(0)
            sys.stdout.write('\nFirst Command Failed:\n' )
            sys.stdout.flush()
            return False
        elif first_chain == '||':
            sys.stdout.write(Fore.RED + f'\nFirst Command Failed:\n' + Style.RESET_ALL)
            sys.stdout.write(Fore.YELLOW + f'\n\t:{return_value}' + Style.RESET_ALL) 
            sys.stdout.flush()
            ch_order.pop(0)
            return True
            

if __name__=='__main__':

    os.system('cls' if os.name == 'nt' else 'clear')
    
    shell = Shell()