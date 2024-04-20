import aidds.sys.messages as msg
from aidds.sys.utils.trace import get_caller, get_error


class AppException(Exception):
    """ Custom exception handling class for exceptions raised within the program.
        When an exception occurs, 
        output file[line number] + function(class) +  error message

    Args:
        exception (Exception or str): Exception object or error string
        
    Output Example:
    
    """
    def __init__(self, exception=None):
        self._error_endswith = msg.exception.sys.error_endswith
        self._head_message = msg.exception.sys.head_message
        self._message = ''
        
        if isinstance(exception, str):
            # Handling of errors occurring internally 
            # during program execution,
            # In which case it comes in as a string 
            # rather than an instance of the Execption class
            self._message = f'\n{exception}'
        else:
            # Convert Exception object to string
            self._message = str(exception)
            # Get error information
            self._caller = f'[{get_caller()}]'
            if self._message.endswith(self._error_endswith):
                # If it came through AppException,
                # Only add info about the transit function(class)
                self._message = self._caller + self._message
            else:
                # First time, caller + err_message + err_endswith
                self._message = f'{self._caller}\n' \
                    f'{get_error(self._message)}{self._error_endswith}'
        super().__init__(self._message)
        
    def print(self):
        # Error endswith remove
        message = self._message[:-3] \
            if self._message.endswith(self._error_endswith) \
                else self._message
        print(f'{self._head_message}{message}')

    
