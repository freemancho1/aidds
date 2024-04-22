import re
import inspect
import traceback

import aidds.sys.config as cfg


def get_caller(is_display=False) -> tuple[str, str]:
    """ Return function and file info
        When called with 'a() -> b() -> get_caller()',
        - it returns information about the 'a()' function or class.function,
        - while the 'b()' is typically used for logging or exceptions.

    Args:
        is_display (bool, optional): 
            Turns on/off the functionality to sequentially display 
            the function call path up to the point 
            where this function is called.
            Defaults to False.

    Returns:
        # tuple[str1, str2]: 
        #     - str1: a() function or class.function name
        #     - str2: In 'filename[line number]', called b() from a()
        ##
        # This function will not provide file information data in the future.
        # As of 2024.4.18
        str: a() function or class.function name
    """
    
    # Gets the stack trace leading up to the invocation of this func.
    stack = inspect.stack()
    # Display stack trace
    if is_display:
        for i, s in enumerate(iterable=stack):
            print(f'{i:>3} {s}')
            
    # 0: get_caller(), 1: b(), 2: a() function info
    caller_frame = stack[2]
    caller_function = caller_frame.function
    if caller_frame.frame.f_locals.get('self'):     # if class:
        class_info = caller_frame.frame.f_locals['self']
        caller_function = f'{class_info.__class__.__name__}.{caller_function}'
    # Get file info(with line number)
    # This function will not provide file information data in the future.
    # As of 2024.4.18
    # caller_file_info = f'{caller_frame.filename}[{caller_frame.lineno}]'
    
    # return caller_function, caller_file_info
    return caller_function
    
def get_error(e_msg=None) -> str:
    """ Returns the error information that occurred.

    Args:
        e_msg (Exception, required): 
            Used directly when there is no error message 
            during error information creation,
            taken from the 'e' value in the 'except Exception as e:' code block.
            Defaults to Exception.

    Returns:
        str: Returns the error information.
            Example: (represented as a single string over two lines as below.)
                /../my_main.py[7]: a = 10/0
                ZeroDivisionError: division by zero
    """
    
    # Get full trace of error events
    traces = inspect.trace()
    # Iterates from the last to 0
    # for error_idx in range(len(traces)-1, -1, -1):
    #     error_pos = traces[error_idx]
    #     error_filename = error_pos.filename
    #     # if the error location is within an open-source(site-packages), skip
    #     if cfg.sys.utils.trace.skip_lib in error_filename:
    #         continue
    #     else:
    #         break
    error_pos = traces[0]
    error_filename = error_pos.filename
        
    # Get error informations(line number, func_name(or class_name.func_name))
    error_lineno = error_pos.lineno
    error_function = error_pos.function
    if 'self' in error_pos.frame.f_locals:  # if class:
        error_class = error_pos.frame.f_locals['self'].__class__.__name__
        error_function = f'{error_class}.{error_function}'
        
    # Open the file and get the code block where the error occurred.
    with open(error_filename, 'r') as file:
        lines = file.readlines()
        error_content = lines[error_lineno-1].strip() \
            if 0 < error_lineno <= len(lines) else ''
    
    # Get error message
    error_message = _get_error_message(traceback.format_exc())
    # If there is no error message, return e_msg
    error_message = error_message if error_message else e_msg
    
    return f'{error_filename}[{error_lineno}]: {error_content}\n{error_message}'
    
def _get_error_message(error_trace=None) -> str:
    """ Returns the error message from the error trace
        using regular expressions. 
        
    Args:
        - error_trace (str, required): error trace information
            Example error_trace:
                Traceback (most recent call last):
                File "/tmp/ipykernel_136739/358233475.py", line 2, in <module>
                    a = 10/0
                ZeroDivisionError: division by zero
    """
    # Pattern to extract errors from error trace
    pattern = cfg.sys.utils.trace.error_pattern
    # Find the part matched with the error pattern in the error trace
    match = re.search(pattern=pattern, string=error_trace)
    error_message = match.group().strip('\n') if match else ''
    return error_message
