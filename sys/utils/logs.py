import uuid
from datetime import datetime

import aidds.sys.config as cfg
import aidds.sys.messages as msg


class ModelingLogs:
    # 중첩 로그의 깊이를 저장하는 정형변수
    depth = -1
    
    def __init__(self, code='NONE'):
        self.uuid = str(uuid.uuid4()).split('-')[-1]
        self.is_log_display = cfg.IS_LOG_DISPLAY
        self.start_time = datetime.now()
        self.code = code
        self.msg = msg.LOGs['MAIN'][code]
        ModelingLogs.depth += 1
        self.depth = ModelingLogs.depth
        self._start()
        
    def _start(self):
        self._print(self._get_message('START'))
        
    def mid(self, dcode=None, value=None):
        # dcode: details code
        out_msg = ''
        if dcode is not None:
            out_msg = msg.LOGs['SUB'][self.code][dcode]
            if value is not None:
                out_msg += f': {value}'
        else:
            if value is not None:
                out_msg = value
        self._print(out_msg, depth=self.depth+1)
        
    def stop(self):
        ptime = datetime.now() - self.start_time
        self._print(self._get_message('STOP'), ptime)
        ModelingLogs.depth -= 1
    
    def _get_message(self, mode='START'):
        tail = msg.LOGs['SYS'][mode]
        return tail if self.code=='NONE' else f'{self.msg} {tail}'
    
    def _print(self, pmsg, ptime=None, depth=None):
        # pmsg: print message, ptime: processing time
        if not self.is_log_display:
            return
        dspace = '  ' * (self.depth if depth is None else depth)
        print(f'[{self.uuid}][{datetime.now()}] {dspace}{pmsg}', end='')
        print('' if ptime is None else f', {msg.LOGs["SYS"]["TOTAL"]}: {ptime}')
        
        
class ServingLogs:
    pass