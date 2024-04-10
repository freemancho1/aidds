from aidds.sys.utils.trace_info import get_caller_info, get_error_info


class AiddsException(Exception):
    
    ERROR_ENDSWITH = '***'
    
    def __init__(self, message=None): 
        if isinstance(message, str):
            self._message = f'\n{message}'
        else:
            self._message = str(message)
            self._caller_name = f'[{get_caller_info()}]'
            if self._message.endswith(self.ERROR_ENDSWITH):
                self._message = self._caller_name + self._message
            else:
                self._message = f'{self._caller_name}\n' \
                                + get_error_info(self._message) \
                                + self.ERROR_ENDSWITH
        super().__init__(self._message)
        
    def print(self):
        if self._message.endswith(self.ERROR_ENDSWITH):
            message = self._message[:-3]
        else:
            message = self._message
        print(f'\n:::AiddsError {message}\n')