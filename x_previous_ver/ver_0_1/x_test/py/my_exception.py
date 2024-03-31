from aidds.x_previous_ver.ver_0_1.x_test.py.my_utils import get_caller_name2, get_error_info

ERR_ENDSWITH = '***'

class MyException(Exception):
    def __init__(self, msg=None):
        self._msg = None
        msg = str(msg)
        call_fn = f'[{get_caller_name2()}]'
        if msg.endswith(ERR_ENDSWITH):
            self._msg = call_fn + msg
        else:
            self._msg = f'{call_fn}\n' + get_error_info(msg) + ERR_ENDSWITH
        super().__init__(self._msg)
        
    def print(self):
        out_msg = self._msg[:-3] if self._msg.endswith(ERR_ENDSWITH) else self._msg
        print(f'Error: {out_msg}')
    
    # @classmethod
    # def print_err(msg=None):
    #     out_msg = msg[:-3] if msg.endswith(ERR_ENDSWITH) else msg
    #     print(out_msg)
        
        
class MyLog:
    def __init__(self):
        pass
    
    def mid(self):
        print(f'Log.mid: {get_caller_name2(is_display=False)}')