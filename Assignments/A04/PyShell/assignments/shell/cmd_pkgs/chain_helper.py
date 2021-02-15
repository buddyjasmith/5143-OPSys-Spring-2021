
class ChainHelper():
    '''
    :Class: ChainHelper
    :Constructor: parametrized
    :Arguments: cmd_in: Arguments passed form shell.py
    :Methods: ChainHelper(self,cmd_in)
            : __split_cmd(self)
            : __trim_chain_cms(self)
            : __count_chains(self)
            : get_chain_cmds(self)
            : get_chain_order(self)
    :Members: cmd_in: store original values pass to constructor
    :       : chain_cmds: store split commands
    :       : chain_order: order of the chains passed
    :       : chain_list: stores reference of recognized/accepted chains
    :Description: This class is a helper function for shell.py If an command
    :           : is given with chanin operators, this class will split the 
    :           : command into mulitple segments, count the number of operators
    :           : and provide the caller with access these values
    '''
    def __init__(self, cmd_in):
        '''
        :**********************************************************************
        :Method: ChainHelper(cmd_in)
        :Parameters: cmd_in
        :Returns: na
        :Description: sets internal data memeber to cmd_in and begins the 
        :           : process of splitting cmd_in into mulitple commands
        :           : if present
        :Problems: ??
        :To-Dos: ?? Maybe combine this class with ArgParser
        :**********************************************************************
        '''
        self.cmd_in = cmd_in
        self.chain_cmds =[]
        self.chain_order = []
        self.chain_lists = [
            '>',
            '<',
            '>>',
            '|',
            '||',
            '&&',
            '&'
        ]
        for i in (self.__split_cmds()):
            self.chain_cmds.append(i)
        self.__trim__chain__cmds()
        
    def __split_cmds(self):
        '''
        :**********************************************************************
        :Method: __split_cmds: private
        :Parameters: none
        :Returns: na
        :Description: the method looks though the string and splits them into
        :           : a list based upone chain operators
        :
        :Problems: no
        :To-Dos: none
        :**********************************************************************
        '''
        indices = [i for i, x in enumerate(self.cmd_in)if x in self.chain_lists]
        for start, end in zip([0, *indices], [*indices, len(self.cmd_in)]):
            yield self.cmd_in[start: end +1]

    def __trim__chain__cmds(self):
        '''
        :**********************************************************************
        :Method: __split_cmds: private
        :Parameters: none
        :Returns: na
        :Description: the method removes chain operators from the commands and 
        :           : stores them in a list for the user to acces in call shell
        :
        :Problems: no
        :To-Dos: none
        :**********************************************************************
        '''
        tempList = []
      
        for lst in self.chain_cmds:
            temp = [i for i in lst if i not in self.chain_lists]
            tempList.append(temp)
            
        self.__count_chains()
        
        self.chain_cmds = tempList
        
    def __count_chains(self):
        '''
        :**********************************************************************
        :Method: __count_chains, private
        :Parameters: none, self
        :Returns: na
        :Description: the method appends chains to the chain_order list
        :
        :Problems: no idea why I did it this way, but when I tried to streamline
        :        : to many issues arose.  
        :To-Dos: Streamline this into another function
        :**********************************************************************
        '''
        for item in self.cmd_in:
            if item in self.chain_lists:
                self.chain_order.append(item)
         
    def get_chain_cmds(self):
        '''
        :**********************************************************************
        :Method: __get_chain_cmds: public
        :Parameters: none
        :Returns: list
        :Description: get method for the list chain_cmds
        :
        :Problems: no
        :To-Dos: none
        :**********************************************************************
        '''
        return self.chain_cmds  
    def get_chain_order(self):
        '''
        :**********************************************************************
        :Method: get_chain_order: public
        :Parameters: none
        :Returns: na
        :Description: returns the chains seperated from commands in a list
        :
        :Problems: no
        :To-Dos: none
        :**********************************************************************
        '''
        return self.chain_order