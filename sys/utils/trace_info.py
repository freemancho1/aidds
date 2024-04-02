import re
import inspect
import traceback


def get_caller_info(is_file_info=False, is_display=False):
    """ 이 함수를 호출한 함수를 호출한 함수의 정보를 리턴한다.
        일반적으로 로그출력이나, 예외사항 처리에서 사용한다.
    Args:
        is_file_info (bool, optional):
            함수명에 추가적으로 파일정보를 리턴할 여부를 설정
        is_display (bool, optional): 
            이 함수를 호출할 때까지의 함수 호출 경로를 순차적으로 표시하는 
            기능을 On/Off 시킴
    Returns:
        caller_fn_name(str or str, str): 
            이 함수를 호출한 함수의 이름과 파일정보를 리턴한다. 
            이 함수를 호출한 함수가 클래스일 경우 클래스명.함수이름을 리턴함.
            예:
                함수명
                클래스명.함수명
                클래스명.함수명, 파일명:호출한_라인번호(is_file_info=True)
    """
    # 이 함수가 호출되기까지의 전체 경로를 가지는 스택을 가져옴
    stack = inspect.stack()
    # 옵션값에 의해 전체 스택을 출력하거나 무시함.
    if is_display:
        for i, s in enumerate(stack):
            print(f'{i:>3} {s}')
    
    # 이 함수를 호출한 함수를 호출한 함수의 스택 프레임을 가져옴
    # 0: 이 함수(get_caller_name())
    # 1: 이 함수를 호출한 함수
    # 2: 이 함수를 호출한 함수를 호출한 함수
    caller_frame = stack[2]
    # 함수명 추출
    caller_function = caller_frame.function
    # 클래스 메서드인 경우 클래스명 추출
    if caller_frame.frame.f_locals.get('self'):
        class_info = caller_frame.frame.f_locals['self']
        caller_function = f'{class_info.__class__.__name__}.{caller_function}'
    
    # 파일정보(파일명:호출라인) 추출
    caller_file_info = f'{caller_frame.filename}[{caller_frame.lineno}]'

    if is_file_info:
        return caller_function, caller_file_info
    else:    
        return caller_function
    
def get_error_info(e_msg=None):
    """ 발생한 에러 정보를 리턴한다.
    Args:
        e_msg (str, required): 
            에러 정보를 생성하는 과정에서 에러 메시지가 없을 때 바로 사용하기 위해,
            except Exception as e: 코드에서 'e' 값을 가지고 옴
    Returns:
        str: 
            에러 정보를 리턴함
            예: (아래와 같이 하나의 스트링 두 줄로 표현된다.)
                /../my_main.py[7]: a = 10/0
                ZeroDivisionError: division by zero
    """     
    # 이 함수를 호출될 때까지의 전체 이벤트가 저장된 트레이스를 불러옴
    trace_info = inspect.trace()
    # 에러 위치를 가져옴(에러는 보통 마지막에 저장됨)
    error_pos = trace_info[-1]
    
    # 다양한 에러 위치의 정보 추출
    error_filename = error_pos.filename
    error_lineno = error_pos.lineno
    # 함수명(또는 클래스명.함수명) 정보 추출
    error_function = error_pos.function
    if 'self' in error_pos.frame.f_locals:
        error_class = error_pos.frame.f_locals['self'].__class__.__name__
        error_function = f'{error_class}.{error_function}'
        
    # 해당 파일을 읽어 에러가 발생한 줄의 코드 등을 불러옴
    with open(error_filename, 'r') as file:
        lines = file.readlines()
        error_content = lines[error_lineno-1].strip() \
            if 0 < error_lineno <= len(lines) else ''
            
    # 에러 메시지 가져오기
    error_message = _get_error_message(traceback.format_exc())
    # 에러 메시지가 없으면 호출될 때 가져옴 에러 메시지를 그대로 리턴함
    error_message = e_msg if error_message == '' else error_message
    
    # 결과반환
    return f'{error_filename}[{error_lineno}]: {error_content}\n{error_message}'
    
def _get_error_message(error_message=None):
    # 에러 메시지에서 추출할 에러 패턴
    pattern = r'\n[A-Z].*?\n'
    # 정규식에서 에러 패턴과 매치되는 부분 찾기
    match = re.search(pattern=pattern, string=error_message)
    return match.group().strip('\n') if match else ''