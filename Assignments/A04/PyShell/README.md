# PySH
## Buddy Smith
## Leila Kalantari

## Project : A04
PyShell is a terminal shell written in Python by Leila Kalantari and Buddy Smith

## Run command:
python3 shell.py
**PySh operates erratically if initiated in VSCode Terminal.  To avoid this use an actual terminal.  Such as Iterm2**
### Commands
|Command|Author|Usage|Bugs|Status|
|---|---|---|---|---|
| cat| Leila   | cat [file]  |   |:heavy_check_mark:   |
| cd   | Buddy   | cd [path]  |   | :heavy_check_mark:  |
| chmod| Buddy/Leila | chmod [ugo +-= rwx] [octal] [path] ||:heavy_check_mark:|
| cp   | Buddy  | cp [src] [dest]  |   | :heavy_check_mark:  |
|grep| Buddy| grep 'exp' [paths]||:heavy_check_mark:||
| head| Buddy   | head [-n] [path]  |   |:heavy_check_mark:   |
| history| Buddy| history   |   |:heavy_check_mark:   |
|less| Buddy|||:x:|
| ls| Buddy | ls [-lah] [paths]  | I think I have the bugs worked out, but everyday something changes  |:heavy_check_mark:   |   
| mkdir|Buddy| mkdir [newpath]  |   |:heavy_check_mark:   | 
|mv| Buddy|mv [src] [destination]||:heavy_check_mark:|
|pwd| Buddy|pwd||:heavy_check_mark:|
|rm| Buddy|rm [-r -f] [path]|I have implemented 2 different methods for directory deletion, I seem to flip flop back and forth between the 2 each erroring. At time of submission working.|:heavy_check_mark:|
|rmdir| Buddy| rmdir [-r -f] [path] ||:heavy_check_mark:|
|sort | Leila|sort[-C] [file]||:heavy_check_mark:|
|tail | Leila|tail [-n] [file]||:heavy_check_mark:|
|touch| Buddy|touch[path/file] ||:heavy_check_mark:|
|wc | Leila| wc [-C][-l -m -w] [file]|-w displays slightly higher number than bash.  Unable to resolve. Not always consistently buggy|:heavy_check_mark:|
|who| Leila| who ||:heavy_check_mark:|
##### wc and sort implement a '-C' option to sort of count non file related content
### Chain Commands
| Command | Author  | Bugs | Status|
|---|---|---|---|
| > | Buddy | issues when used with sort(fixed) | :heavy_check_mark: |
| >> | Buddy |  |:heavy_check_mark: |
| && | Buddy | | :heavy_check_mark:|
| &#124;&#124; | Buddy | |:heavy_check_mark:|
| &#124;| Buddy | |:heavy_check_mark:|
| < |Buddy | |:x:|
| << | Buddy | |:x: |


### Helper files
|File|Author|Bugs|Usage|Status|
|---|---|---|---|--|
|ArgParse| Buddy||Internal Usage|:heavy_check_mark:|
|ChainHelper| Buddy||Internal Usage|:heavy_check_mark:|
|ChainHelper| Buddy||Internal Usage|:heavy_check_mark:|
|ReturnStatus| Buddy||Internal Usage|:heavy_check_mark:|
|Shell| Buddy||Internal Usage|:heavy_check_mark:|


#### Dependencies: pip3 install readchar, pip3 install PrettyTable

#### External Sources:
    http://www.linfo.org/byte.html : I had trouble getting exact readout of byte conversion correctly, utilized in ls.  Simple task, but my method one was wrong.
    
