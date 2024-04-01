import uuid
from datetime import datetime

import aidds.sys.config as cfg
import aidds.sys.messages as msg
from aidds.sys.utils.exception import AiddsException


class ModelingLogs:
    # 중첩 로그의 깊이를 저장하는 정형변수
    _depth = -1

    def __init__(self, code='NONE'):
        try:
            self._uuid = str(uuid.uuid4()).split('-')[-1]
            self._is_display = cfg.IS_MODELING_LOG_DISPLAY
            self._start_time = datetime.now()
            self._code = code
            self._message = msg.LOGs['MAIN'][self._code]
            ModelingLogs._depth += 1
            self._depth = ModelingLogs._depth
            self._start()
        except AiddsException as ae: 
            raise AiddsException(ae)
        except Exception as e: 
            raise AiddsException(e)
        
    def _start(self):
        try:
            self._print(self._get_message('START'))
        except AiddsException as ae: 
            raise AiddsException(ae)
        except Exception as e: 
            raise AiddsException(e)
        
    def mid(self, mcode=None, value=None):
        # mcode: message code
        try:
            message = ''
            if mcode is not None:
                message = msg.LOGs['SUB'][self._code][mcode]
                if value is not None: message += f': {value}'
            else:
                if value is not None: message = value
            self._print(message, depth=self._depth+1)
        except AiddsException as ae: 
            raise AiddsException(ae)
        except Exception as e: 
            raise AiddsException(e)
        
    def stop(self):
        try:
            ptime = datetime.now() - self._start_time
            self._print(self._get_message('STOP'), ptime=ptime)
            ModelingLogs._depth -= 1
        except AiddsException as ae: 
            raise AiddsException(ae)
        except Exception as e: 
            raise AiddsException(e)
    
    def _get_message(self, mode='START'):
        try:
            tail = msg.LOGs['SYS'][mode]
            return tail if self._code == 'NONE' else f'{self._message} {tail}'
        except Exception as e: 
            raise AiddsException(e)
        
    def _print(self, message=None, ptime=None, depth=None):
        # ptime: processing time
        try:
            if not self._is_display: return
            depth_space = '  ' * (self._depth if depth is None else depth)
            print(
                f'[{self._uuid}][{datetime.now()}] {depth_space}{message}', end=''
            )
            print(
                '' if ptime is None else f', {msg.LOGs["SYS"]["TOTAL"]}: {ptime}'
            )
        except Exception as e: 
            raise AiddsException(e)
        
        
class ServingLogs:
    pass