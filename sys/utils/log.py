import uuid
from datetime import datetime

import aidds.sys.config as cfg
import aidds.sys.message as msg
from aidds.sys.utils.trace import get_caller, get_error


class ModelingLogs:
    # 중첩 로그의 깊이를 저장하는 정형변수
    _depth = -1
    
    def __init__(self, message=None):
        # 로그별 고유Key값 생성
        self._uuid = str(uuid.uuid4()).split('-')[-1]
        # 로그 출력 여부
        self._is_display = cfg.sys.case.log_display.modeling
        # 로그 시작시간 저장(나중에 최종 처리시간 계산 시 사용)
        self._start_time = datetime.now()
        # stop()함수에서 사용하기 위해 저장해 둠
        self._message = message
        # 로그 depth별 깊이를 표현하기 위해 앞 공백 표시하는데
        # 로그가 중첩될수록 앞의 공백이 추가됨
        ModelingLogs._depth += 1
        # 현재 로그의 깊이를 저장
        self._depth = ModelingLogs._depth
        self._start()
        
    def _start(self):
        self._print(message=f'{self._message} {msg.log.sys.start}')
        
    def mid(self, message=None, value=None):
        output = ''
        if message is not None:
            output = message
            if value is not None: output += f': {value}'
        else:
            if value is not None: output = value
        # 현재 로그의 기본 깊이보다 한 단계 추가해서 중간 로그를 출력함
        self._print(message=output, depth=self._depth+1)
        
    def stop(self):
        ptime = datetime.now() - self._start_time
        message = f'{self._message} {msg.log.sys.stop}'
        self._print(message=message, ptime=ptime)
        # 종료시점에 중첩된 값을 하나 빼야함
        # (이 부분 때문에 stop()함수는 반드시 실행되어야 함)
        ModelingLogs._depth -= 1
        
    def _print(self, message=None, ptime=None, depth=None):
        if not self._is_display: 
            return
        # 중첩값에 의해 앞 공백 추가
        depth_space = '  ' * (self._depth if depth is None else depth)
        # 기본 메시지 출력
        output = f'[{self._uuid}][{datetime.now()}] {depth_space}{message}'
        # 완료시점(ptime is not None)이면 총 처리시간 표시
        output += '' if ptime is None else f'{msg.log.sys.total} {ptime}'
        print(output)
        

def service_logs(message=None, value=None):
    if not cfg.sys.case.log_display.service:
        return
    output = f'[{datetime.now()}]'
    output += '' if message is None else f' {message}'
    output += '' if value is None else f'{value}'
    
    
def route_error_logs(error=None):
    _head_message = msg.exception.sys.head_message
    output = f'{_head_message}[{get_caller()}]\n{get_error(str(error))}\n'
    print(output)
        