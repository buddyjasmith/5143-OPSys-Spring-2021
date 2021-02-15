class ReturnStatus:
    '''
    :Class: ReturnStatus
    :Constructor: Default
    :Parameters: none
    :Members: return_status
    :       : cwd
    :       : return_values
    :Methods: set_return_status
    :       : get_return_status
    :       : set_return_values
    :       : get_return_values
    :       : get_cwd
    :       : set_cwd
    :Description: A simple object to return the status of function calls
    '''
    def __init__(self):
        self.return_status = 0
        self.cwd = ''
        self.return_values = ''
    def set_return_status(self, value):
        self.return_status = value
    def set_cwd(self, path):
        self.cwd = path
    def set_return_values(self, values):
        self.return_values += values
    def get_return_status(self):
        return self.return_status
    def get_cwd(self):
        return self.cwd
    def get_return_values(self):
        return self.return_values