'''Dr griffin
code
'''
'''
Name
     wc
Discription 
            wc filename    #counts num of lines words charecters 
            wc -l filename #counts num of lines 
            wc -m filename #counts num of words
            wc -w filename #counts num of char 
            sc -C [contents] # performs wc on contents rather than files
            -C must be leading flag if this option is chosen, by all other flags are by default when -C is chosen
'''
import re  # Regular Expression(RE) Syntax AND
import sys
import os
from cmd_pkgs.arg_parser import ArgParse
from cmd_pkgs.return_status import ReturnStatus
# "re" module included with Python primarily used for string searching and manipulation
## And it is necessory for using regex (findall()) function
from cmd_pkgs.return_status import ReturnStatus
arg_dict = {
    'l': False,
    'm': False,
    'w': False,
}
def wc(args, cwd):
    '''
    :Function:      wc
    :Usage:         wc OPTION... [FILE]...
    :Author:        Buddy Smith & Leila Kalantari
    :Parameters:    args: parameters from command line
    :               cwd: current working directory
    :Description:   Count Number of Lines, Words, and Characters
    :Todo:          Test more
    :Returns:       Returns the ReturnStatus object consisting  of status, return values, and the cwd
    :Bugs:          None at this time
    '''
    
    arg_parse = ArgParse(args, arg_dict, cwd, __doc__)
    flags = arg_parse.get_flags()
    rs = ReturnStatus()
    rs.set_cwd(cwd)
    
    directories = arg_parse.get_directories()
    big_C = '-C' in args
    if big_C:
        passed_content = args[2:]
        wc = 0
        numlines = len(passed_content)
        characters = [len(i) for i in passed_content]
        characters = sum(characters)
        for item in passed_content:
            wc += len(item.split())
        rs.set_return_values(str(numlines) +' lines\n')
        rs.set_return_values(str(characters)+ ' characters\n')
        rs.set_return_values(str(wc) + ' words\n')
        rs.set_return_status(1)
        return rs

    for i in directories:
        if os.path.isdir(i):
            rs.set_return_status(0)
            rs.set_return_values(f'wc: {i} is a directory')
            return rs
    if not flags:
        filenum = 0
        for p in directories:
            try:
                with open(directories[filenum], "r") as f:
                    lines = f.readlines()  # Use f.read() combined with splitlines()The splitlines()
                    # method splits a string into a list. The splitting is done at line breaks.
                with open(directories[filenum], "r") as f:
                    words = f.read()
            except FileNotFoundError:
                rs.set_return_status(0)
                rs.set_return_values('No such file or directory')
                return rs
            numlines = str(len(lines))
            #rs.set_return_values(numlines)  # prints number of lines
            numwords = str(len(words.split())) + " "  # Here findall() function is used to count the
            # number of words in the sentence available
            # in a regex module.
            chars = str(len(words))
            temp_str = str(f'{numlines} {numwords} {chars} {os.path.basename(p)}')
            rs.set_return_values(temp_str)
            filenum += 1
        rs.set_return_status(1)
    elif flags:
        # wc-l is getting the number of lines in the file
        temp_list = []
        filenum = 0
        lines = 0
        numwords = 0
        numchar = 0
        for path in directories:
            if 'l' in flags:
                with open(path, "r") as f:
                    lines = f.read().splitlines()
                lines = len(lines)
                lines = str(f'{lines} ')
                temp_list.append(lines)
            if 'm' in flags:
                with open(path, "r") as f:
                    words = f.read()
                numwords = len(re.findall(r'\w+', words))
                numwords = str(f'{numwords} ')
                temp_list.append(numwords)
            if 'w' in flags:
                with open(path, "r") as f:
                    chars = f.read()
                numchar = len(chars)
                numchar = str(f'{numchar} ')
                print(numchar)
                temp_list.append(numchar)
            temp_list.append(os.path.basename(path))
            temp_str = ''
            temp_str = temp_str.join(temp_list)
            rs.set_return_values(temp_str)
    status = 1 if rs.get_return_values() else 0
    rs.set_return_status(1)
    
        # else:
        #     rs.set_return_values("Invalid")
    return rs