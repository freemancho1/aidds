import uuid
from datetime import datetime

from aidds_buy.sys import config as cfg
from aidds_buy.sys import messages as msg
from aidds_buy.sys.utils import get_caller
from aidds_buy.sys.utils import get_error


class ModelingLogs:
    """ Logging output class for the modeling section.
    
    Args:
        code (str): The log message code defined in sys.message,
                    'msg.log.' prefix and '.main' suffix are omitted.

    Static Attributes:
        _depth (int): Data management for the depth of nested log instances.

    Attributes:
        _uuid (str): The unique value of the current log (printed together with the log).
        _is_display (bool): Checks whether logging is enabled.
        _start_time (datetime): Time when the log is created (used for calculating processing time until completion).
        _code (str): The code of the current log (msg.log(o), main(x)).
        _message (str): The main message of the current log.
        _depth (int): The depth of the current log.
    """
    _depth = -1
    
    def __init__(self, code=None):
        # Generate a unique key value for each log.
        self._uuid = str(uuid.uuid4()).split('-')[-1]
        self._is_display = cfg.sys.cond.display_logs.modeling
        self._start_time = datetime.now()
        self._code = f'msg.log.modeling.{code}' if code else 'msg.log.modeling'
        self._main_message = eval(f'{self._code}.main')
        self._start()
        
    def _start(self):
        # To represent the depth of logs, leading spaces are used.
        # If logs are nested, additional leading spaces are added.
        ModelingLogs._depth += 1
        self._depth = ModelingLogs._depth
        
        self._print(message=f'{self._main_message} {msg.log.sys.start}')
        
    def mid(self, code=None, value=None):
        display = ''
        if code:
            display = eval(f'{self._code}.{code}')
            display += f': {value}' if value else ''
        else:
            display = value if value else ''
        # Outputting intermediate logs by adding one more level
        # then the default depth of the current log.
        self._print(message=display, depth=self._depth+1)
        
    def stop(self):
        ptime = datetime.now() - self._start_time
        display = f'{self._main_message} {msg.log.sys.stop}'
        self._print(message=display, ptime=ptime)
        # One level of nested value should be subtracted at the end-point.
        # (Because of this, the stop() function must be executed without fail.)
        ModelingLogs._depth -= 1
    
    def _print(self, message=None, ptime=None, depth=None):
        if not self._is_display:
            return
        # Leading spaces are added according to the magnitude of the nestin value
        leading_spaces = '  ' * (depth if depth else self._depth)
        # Display message
        display = f'[{self._uuid}][{datetime.now()}] {leading_spaces}{message}'
        # Display total processing time
        display += f'{msg.log.sys.total} {ptime}' if ptime else ''
        print(display)


def service_logs(code=None, value=None) -> None:
    """ Logging output class for the service section. """
    if not cfg.sys.cond.display_logs.service:
        return
    display = f'[{datetime.now()}]'
    display += f' {eval(f"msg.log.service.{code}")}' if code else ''
    display += '' if value is None else f' {value}'
    print(display)
    
    
def route_error_logs(error=None) -> None:
    """ Logging output class for the route errors. """
    head_message = msg.exception.sys.head_message
    display = f'\n[{datetime.now()}]'
    display += f'{head_message}[{get_caller()}]\n{get_error(str(error))}\n'
    print(display)



