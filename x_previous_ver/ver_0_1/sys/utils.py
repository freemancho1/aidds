import uuid
import platform
import warnings
import sys
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from datetime import datetime
from sklearn.exceptions import DataConversionWarning, ConvergenceWarning

import aidds.sys.config as cfg
import aidds.sys.messages as msg


class AiddsInit:
    def __init__(self):
        self._set_warnings()
        
    def _set_warnings(self):
        # 엑셀파일 데이터를 읽는 경우 발생할 수 있는 경고(무시가능)
        module = 'openpyxl.styles.stylesheet'
        warnings.filterwarnings('ignore', category=UserWarning, module=module)
        
        # scikit-learn에서 데이터 변환 과정에서 발생할 수 있는 경고로,
        # 일반적으로는 잡는 것을 권하지만, 
        # 데이터 양이 많은 경우 정상적으로 처리된 경우에도 발생할 수 있음
        warnings.filterwarnings(action='ignore', category=DataConversionWarning)
        
        # scikit-learn의 알고리즘이 기본옵션의 반복횟수에서 최적의 성능을 나타내지
        # 못했다는걸 말하는데, 일반적으로 이런 경우 'max_iter' 옵션값을 높여주는
        # 방법을 사용하지만, 그 값을 올려도 안되는 경우가 만음.
        # max_iter를 높이면 처리시간에 영향을 주기 때문에 일단 무시.
        warnings.filterwarnings(action='ignore', category=ConvergenceWarning)
        

class PltInit:
    # matplotlib 사용 시 발생하는 한글문제 등을 해결하기 위해 설정하는 코드로,
    # 쥬피터 노트북에서 이미지 처리할 때 호출하면 됨
    def __init__(self, korean=True, dpi=100):
        # 한글처리 여부와 해상도 지정(시스템 기본값이 100임)
        self.korean = korean
        self.dpi = dpi
        if self.korean:
            self._set_korean()
        self._set_minus()
        self._set_dpi()
        
    def _set_minus(self):
        # Matplotlib x,y축 레이블이 마이너스 일 때, '-'로 표시하도록 설정
        # 이 설정을 하지 않으면 음수 기호가 세모인가로 표시됨
        plt.rcParams['axes.unicode_minus'] = False
        
    def _set_dpi(self):
        # 해상도 지정
        # - 일반적으로 100이면 충분하며, 인쇄용 고해상도가 필요할 때 200 이상 지정
        self.dpi = 100 if self.dpi is None else self.dpi
        plt.rcParams['figure.dpi'] = self.dpi
        
    def _set_korean(self):
        # 기본적인 경우는 아래 4컬럼만 해도 됨
        osName = platform.system()
        fontPath = cfg.WIN_FONT_PATH if osName == 'Windows' else cfg.UBUNTU_FONT_PATH
        fontFamily = fm.FontProperties(fname=fontPath).get_name()
        plt.rcParams['font.family'] = fontFamily
        
        # 위와 같이 해도 안되는 경우
        # Matplotlib에서 자체적으로 관리하는 폰트 캐시에 해당 문자를 추가함
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = [fontFamily]
        
        font_entry = fm.FontEntry(
            fname = cfg.WIN_FONT_PATH if osName == 'Windows' else cfg.UBUNTU_FONT_PATH,
            name = cfg.WIN_FONT_NAME if osName == 'Windows' else cfg.UBUNTU_FONT_NAME
        )
        fm.fontManager.ttflist.insert(0, font_entry)
        
        
class AiddsException(Exception):
    def __init__(self, e_code, value=None, se_msg=None):
        # e_code: error code
        # se_msg: super exception message
        
        # 에러 단계별로 구분하는 구분자('\n')
        self.delimiter = cfg.EXCEPTION_DELIMITER
        try:
            self.msg = msg.EXCEPIONs[e_code]
            self.msg += '' if value is None else f'[{value}]'
            self.msg += '' if se_msg is None else f'{self.delimiter}{se_msg}'
            self.msgs = self.msg.split(self.delimiter)
            self.out_msg = ''
            for m in self.msgs:
                self.out_msg += f'{"  "+m}{self.delimiter}'
            super().__init__(self.out_msg)
        except Exception as e:
            print(f'{msg.EXCEPIONs["EXCEPTION_ERR"]}\n{e}')
            sys.exit(-1)
            
class AiddsServiceException(Exception):
    def __init__(self, emsg=None, smsg=None):
        # emsg: error message
        # smsg: super exception message
        self._emsg = 'Error' if emsg is None else emsg
        self._emsg += '' if smsg is None else f'{smsg}'
        super().__init__(self._emsg)
      
        

class Logs:
    # 중첩 로그의 깊이를 저장하는 정형변수
    depth = -1
    
    def __init__(self, code='NONE'):
        self.uuid = str(uuid.uuid4()).split('-')[-1]
        self.is_log_display = cfg.IS_LOG_DISPLAY
        self.start_time = datetime.now()
        self.code = code
        self.msg = msg.LOGs['MAIN'][code]
        Logs.depth += 1
        self.depth = Logs.depth
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
        Logs.depth -= 1
    
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
        
        
class ServiceLogs:
    def __init__(self, code=None, value=None):
        self._is_display = cfg.IS_SERVICE_LOG_DISPLAY
        self._code = code
        self._start(value=value)
        
    def _start(self, value=None):
        base_msg = msg.SERVICE_LOGs[self._code]
        value_msg = '' if value is None else value
        out_msg = f'{base_msg}{value_msg}'
        self._print(out_message=out_msg, is_start=True)
        
    def mid(self, code=None, value=None, name=None):
        # 중간에 name을 자동으로 추가하는 코드를 추가해
        # 공백 문제로 코드가 복잡해졌는데, 이후 수정할 필요가 있음
        base_msg = '' if code is None \
            else msg.SERVICE_LOGs[f'{self._code}_MID'][code]
        if name is not None:
            # base_msg가 ''인 경우 중간 공백하나 제거하기 위해 코드가 길어짐
            base_msg = f'{self._get_last_name(name)} {base_msg}' \
                if code is not None else self._get_last_name(name)
        value_msg = '' if value is None else value
        out_msg = f'[{self._code}] {base_msg} {value_msg}' \
            if base_msg != '' else f'[{self._code}] {value_msg}'
        self._print(out_message=out_msg)
        
    def _print(self, out_message=None, is_start=False):
        if not (self._is_display or is_start):
            return
        print(out_message)
        
    def _get_last_name(self, name=None):
        return f'[{name.split(".")[-1].upper()}]'
