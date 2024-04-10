import aidds.sys.message as msg
from aidds.sys.utils.trace import get_caller, get_error


class AiddsException(Exception):
    def __init__(self, message=None):
        self._error_endswith = msg.exception.sys.error_endswith
        self._head_message = msg.exception.sys.head_message
        # 프로그램 실행 중간에 자체적으로 발생한 오류에 대한 처리로,
        # 이 부분 Exception 클래스의 인스턴스가 아닌 문자열로 들어옴
        if isinstance(message, str):
            self._message = f'\n{message}'
        else:
            # Exception 클래스의 인스턴스를 문자열로 변환
            self._message = str(message)
            # 에러가 발생한 (클래스)함수의 정보를 불러옴
            self._caller = f'[{get_caller()}]'
            if self._message.endswith(self._error_endswith):
                # AiddsException을 거쳐서 온 경우는 
                # 경유하는 (클래스)함수의 정보만 추가함
                self._message = self._caller + self._message
            else:
                # 최초로 AiddsException을 거치는 경우는
                # 에러가 발생한 (클래스)함수를 첫 줄에 표시하고,
                # 에러 정보를 다음줄에 표시함(경유했다는 표시('***') 추가)
                self._message = f'{self._caller}\n' \
                                + get_error(self._message) \
                                + self._error_endswith
        super().__init__(self._message)
        
    def print(self):
        # 마지막에 AiddsException에서 추가한 경유 표시('***')를 제거
        message = self._message[:-3] \
            if self._message.endswith(self._error_endswith) \
                else self._message
        print(f'{self._head_message}{message}\n')