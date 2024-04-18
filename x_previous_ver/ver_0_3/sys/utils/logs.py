import uuid
from datetime import datetime

import aidds.sys.config as cfg
import aidds.sys.message as msg
from aidds.sys.utils.trace import get_caller, get_error


class ModelingLogs:
    """ 모델링 부분 로그 출력 클래스 
    
    Args:
        code             (str): sys.message에 정의된 로그메시지 코드,
                                앞에 붙는 'msg.log.'과 뒤에 붙은 '.main'은 생략함
    
    Static Attributes:
        _depth           (int): 로그 인스턴스 중첩도 관리 데이터
    Attributes:
        _uuid            (str): 현재 로그의 고유값(로그 출력시 같이 출력됨)
        _is_display     (bool): 로그 출력여부 체크
        _start_time (datetime): 로그 생성시간(종료시점까지의 처리시간 계산에 활용)
        _code            (str): 현재 로그의 코드(msg.log(o), main(x))
        _message         (str): 현재 로그의 main 메시지
        _depth           (int): 현재 로그의 깊이
    """
    _depth = -1
    
    def __init__(self, code=None):
        # 로그별 고유Key값 생성
        self._uuid = str(uuid.uuid4()).split('-')[-1]
        self._is_display = cfg.sys.case.log_display.modeling
        self._start_time = datetime.now()
        self._code = f'msg.log.{code}'
        self._message = eval(f'{self._code}.main')
        # 로그 depth별 깊이를 표현하기 위해 앞 공백 표시하는데
        # 로그가 중첩될수록 앞의 공백이 추가됨
        ModelingLogs._depth += 1
        self._depth = ModelingLogs._depth
        self._start()
        
    def _start(self):
        self._print(message=f'{self._message} {msg.log.sys.start}')
        
    def mid(self, code=None, value=None):
        output = ''
        if code is not None:
            output = eval(f'{self._code}.{code}')
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
        

def service_logs(code=None, value=None):
    """ 모델링 부분 로그 출력 클래스 
    
    Args:
        code     (str): sys.message에 정의된 로그메시지 코드,
                        앞에 붙는 'msg.log.service.'는 생략함
        value (object): 상황에 따라 변경되는 값(숫자, 문자, 튜플 등)
    """
    if not cfg.sys.case.log_display.service:
        return
    output = f'[{datetime.now()}]'
    output += '' if code is None else f' {eval(f"msg.log.service.{code}")}'
    output += '' if value is None else \
        f' {value}' if code is None else f'{value}'
    print(output)
    
    
def route_error_logs(error=None):
    _head_message = msg.exception.sys.head_message
    output = f'{_head_message}[{get_caller()}]\n{get_error(str(error))}\n'
    print(output)
        