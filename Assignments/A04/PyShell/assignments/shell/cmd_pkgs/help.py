'''

ALL COMMANDS AVAILABLE:

NAME:
    cat - display a file and concatenate file1 and file2 to file0
Flags:
    -d : Cat entire directory
SYNOPSIS:
    cat  [file],[file1 file2 >file0]
DESCRIPTION:
    display a file and concatenate file1 and file2 to file0

*********************************************************************    
NAME:
    cd - Change the shell working directory.

SYNOPSIS:
    cd  [dir]

DESCRIPTION:
    Change the shell working directory.

    Change the current directory to DIR.  The default DIR is ~
*********************************************************************
Name: 
    cp
Usage:
    cp [source] [destination]
Description:
    copies one file/folder to a new destination
*********************************************************************
Name: Grep
SYNOPSIS
       grep [OPTION...] PATTERNS [FILE...]
Flags:  
    -l supress normal output.  Instead, print the name of each input file
       where the matching pattern was found.  
**********************************************************************
Name
    history
Usage: history
Returns a list of items the user has executed in the pyshell.
The user can append an item of the list with ! to call that line from 
history.
ex: !1 - returns the first command from the history list
**********************************************************************
NAME:
       ls - list directory contents
SYNOPSIS:
       ls [OPTION]... [FILE]...
DESCRIPTION:
       List information about the FILEs (the current directory by
       default).
***********************************************************************
NAME:  mkdir
Usage: mkdir [path]
mkdir - make a new directory in the path supplied by user
************************************************************************
Name:
    mv
SYNTAX:
      mv [source] [destination]
      mv [options]... Source Dest
      mv [options]... Source... Directory
Description:
If the last argument names an existing directory, 'mv' moves each other 
given file into a file with the same name in that directory. 
Otherwise, if only two files are given, it renames the first as the second. 
It is an error if the last argument is not a directory 
and more than two files are given.
**************************************************************************
Name: 
    pwd
Description:
    Print the current directory of the user
***************************************************************************
Name:
    rm
Usage:
    rm [OPTION]... FILE... 
Flags:
    -f :Force removal of files
    -r: remove directories and their contents recursively 
Description:
    Used to delete file/folders from directory: Non empty folder must use
    the -r or -f to remove folders and contents
****************************************************************************
Name
    rmdir - remove empty directories
Synopsis
    rmdir [OPTION]... DIRECTORY..
Flags
    - 'f' Force deletion of non empty directory
    - 'r' recursively delete contents of non empty directory
****************************************************************************
NAME:
    sort - sorts files
SYNOPSIS:
    sort [-C] [file]
Flags: 
    -C: sorts contents passed rather than a file
DESCRIPTION:
    sorts the contents of a text file, line by line.
*****************************************************************************
NAME
    sort - sorts files
SYNOPSIS
    sort [-C] [file]
Flags: -C: sorts contents passed rather a file
DESCRIPTION
    sorts the contents of a text file, line by line.
*****************************************************************************
Name: tail
Usage: tail [-n] [paths]
Flags:  -n : number of lines to read
Description: print last n number of lines from a file
******************************************************************************
Command: touch [path/filename]
Description: creates a path in the given path/filename
******************************************************************************
Name
     wc
Discription 
            wc filename    #counts num of lines words charecters 
            wc -l filename #counts num of lines 
            wc -m filename #counts num of words
            wc -w filename #counts num of char 
            sc -C [contents] # performs wc on contents rather than files
            -C must be leading flag if this option is chosen, by all other 
               flags are by default when -C is chosen
*****************************************************************************
NAME
    who - sorts files
SYNOPSIS
    who [options] [filename]
DESCRIPTION
    displays users who are currently logged on.
*****************************************************************************
'''

from cmd_pkgs.return_status import ReturnStatus

def help(args, cwd):
    rs = ReturnStatus()
    rs.set_cwd(cwd)
    rs.set_return_values(str(__doc__))
    rs.set_return_status(1)
    return rs