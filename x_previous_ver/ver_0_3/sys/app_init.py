import platform
import warnings
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from sklearn.exceptions import DataConversionWarning, ConvergenceWarning

import aidds_buy.sys.config as cfg


class AiddsInit: 
    def __init__(self):
        pass
    
    def run(self):
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
        
    def run(self):
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
        os_name = platform.system()
        font_path = cfg.sys.font.win.path if os_name == cfg.sys.font.win.osname \
            else cfg.sys.font.ubuntu.path
        font_family = fm.FontProperties(fname=font_path).get_name()
        plt.rcParams['font.family'] = font_family
        
        # 위와 같이 해도 안되는 경우
        # Matplotlib에서 자체적으로 관리하는 폰트 캐시에 해당 문자를 추가함
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = [font_family]
        
        font_entry = fm.FontEntry(
            fname = cfg.sys.font.win.path if os_name == cfg.sys.font.win.osname \
                else cfg.sys.font.ubuntu.path,
            name = cfg.sys.font.win.name if os_name == cfg.sys.font.win.osname \
                else cfg.sys.font.ubuntu.name
        )
        fm.fontManager.ttflist.insert(0, font_entry)        
