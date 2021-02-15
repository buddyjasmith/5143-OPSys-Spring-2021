import sys
from colorama import Style, Fore
import urllib.request
import socket
import getpass
import os

def print_banner():
    '''
    :Function: banner
    :Parameters: none
    :Returns: none
    :Description: Prints the PyShell banner when the program begin
    :Problems: None at the moment, removed ip address output, in case of not 
    :          being connected to net
    :To-Dos: None
    '''
    # size = os.get_terminal_size()
    # width = size.columns
    sys.stdout.write(Fore.GREEN)
    sys.stdout.write(r'''
        
  ╭━━━╮╱╱╱╭━━━┳╮╱╱╱╱╭╮╭╮
  ┃╭━╮┃╱╱╱┃╭━╮┃┃╱╱╱╱┃┃┃┃
  ┃╰━╯┣╮╱╭┫╰━━┫╰━┳━━┫┃┃┃
  ┃╭━━┫┃╱┃┣━━╮┃╭╮┃┃━┫┃┃┃
  ┃┃╱╱┃╰━╯┃╰━╯┃┃┃┃┃━┫╰┫╰╮
  ╰╯╱╱╰━╮╭┻━━━┻╯╰┻━━┻━┻━╯
  ╱╱╱╱╭━╯┃
  ╱╱╱╱╰━━╯
      
           '''
    
    )
    # cwd = os.path.expanduser('~')
    # sys.stdout.write('\n' + Style.RESET_ALL)
    # sys.stdout.flush()
    # sys.stdout.write(Fore.BLUE + f'User:  { getpass.getuser() }\t\t\n')
    # sys.stdout.write(f'Current Directory:  {cwd}\t\t\n')
    # sys.stdout.flush()
    
    # sys.stdout.flush()
    # sys.stdout.write(Style.RESET_ALL)
    return

