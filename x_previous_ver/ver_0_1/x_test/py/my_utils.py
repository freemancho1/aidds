import re
import inspect
import traceback

def get_caller_name(is_display=False):
    stack = inspect.stack()
    if is_display:
        for i, s in enumerate(stack):
            print(f'{i:>3} {s}')
    caller_frame = stack[1]
    caller_name = caller_frame.function
    return caller_name

def get_caller_name2(check_line=2, is_display=False):
    stack = inspect.stack()
    if is_display:
        for i, s in enumerate(stack):
            print(f'{i:>3} {s}')
    
    # 현재 스택 프레임을 가져옴
    caller_frame = stack[check_line]
    
    # 호출한 함수의 이름을 가져옴
    caller_name = caller_frame.function
    
    # 호출한 위치의 소스코드 파일명과 라인 번호를 가져옴
    source_file = caller_frame.filename
    line_number = caller_frame.lineno
    
    # 파일명과 라인 번호를 조합하여 소스코드 명 생성
    source_code_name = f'{source_file}:{line_number}'
    
    # 클래스 메서드인 경우 클래스명도 포함하여 반환
    if caller_frame.frame.f_locals.get('self'):
        caller_name = caller_frame.frame.f_locals['self']\
            .__class__.__name__ + '.' + caller_name
    
    return caller_name
    # return f'{caller_name} at {source_code_name}'

def get_error_info(msg=None):
    trace_info = inspect.trace()
    error_position = trace_info[-1]

    # 에러가 발생한 파일명과 라인 번호
    file_name = error_position.filename
    line_number = error_position.lineno
    
    # 함수 또는 클래스의 이름
    function_name = error_position.function
    if 'self' in error_position.frame.f_locals:
        class_name = error_position.frame.f_locals['self']\
            .__class__.__name__
        function_name = f'{class_name}.{function_name}'
    
    # 발생한 라인의 내용
    with open(file_name, 'r') as file:
        lines = file.readlines()
        error_line_content = lines[line_number - 1].strip() \
            if 0 < line_number <= len(lines) else ''

    # 에러 코드
    error_code = error_position.code_context[0].strip() if error_position.code_context else ''

    # 에러 메시지 가져오기
    error_msg = extract_error_message(traceback.format_exc())
    if error_msg == '':
        error_msg = msg
    # error_msg = traceback.format_exc()

    # 결과 반환
    error_info = f'{file_name}[{line_number}]: {error_code}\n{error_msg}'
    return error_info
    
def extract_error_message(error_msg):
    pattern = r'\n[A-Z].*?\n'

    # 정규 표현식과 매칭되는 부분 찾기
    match = re.search(pattern, error_msg)

    if match:
        matched_text = match.group()
        # 추출된 패턴 출력
        return matched_text.strip('\n')
    else:
        return ''