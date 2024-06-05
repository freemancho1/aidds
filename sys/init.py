import platform
import warnings
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from sklearn.exceptions import DataConversionWarning, ConvergenceWarning

from aidds_buy.sys import config as cfg


class AppInit:
    def __init__(self):
        self._run()
        
    def _run(self):
        self._set_warnings()
        
    def _set_warnings(self):
        # Warning(can be ignored) that may occur when reading Excel file data
        module = 'openpyxl.styles.stylesheet'
        warnings.filterwarnings('ignore', category=UserWarning, module=module)
        
        warnings.filterwarnings(action='ignore', category=DataConversionWarning)
        warnings.filterwarnings(action='ignore', category=ConvergenceWarning)
        warnings.filterwarnings(action='ignore', category=FutureWarning)
        

class PltInit:
    # Code for resolving issues such as korean font problems when using matplotlib
    # - Call when processing images in Jupyter Notebook
    def __init__(self, dpi=100):
        self._run()
        
    def _run(self):
        # Korean font setting
        self._set_korean()
        # Minus setting
        self._set_minus()
        # Specify resolution
        self._set_dpi()
        
    def _set_korean(self):
        # The basic case only requires the following 5 columns
        os_name = platform.system()
        font_path = cfg.sys.font.win.path if os_name == cfg.sys.font.win.osname \
            else cfg.sys.font.ubuntu.path
        font_family = fm.FontProperties(fname=font_path).get_name()
        plt.rcParams['font.family'] = font_family
        
        # If the above method does not work
        # Add the corresponding character to the font cache managed by Matplotlib
        plt.rcParams['font.family'] = cfg.sys.font.font_family
        plt.rcParams[f'font.{cfg.sys.font.font_family}'] = [font_family]
        
        font_entry = fm.FontEntry(
            fname = cfg.sys.font.win.path if os_name == cfg.sys.font.win.osname \
                else cfg.sys.font.ubuntu.path,
            name = cfg.sys.font.win.name if os_name == cfg.sys.font.win.osname \
                else cfg.sys.font.ubuntu.name
        )
        fm.fontManager.ttflist.insert(0, font_entry)      
        
    def _set_dpi(self):
        # Specify resolution
        # - Typically, 100 is sufficient, 
        #   and specify 200 or more for high-resolution printing needs
        self.dpi = 100 if self.dpi is None else self.dpi
        plt.rcParams['figure.dpi'] = self.dpi
        
    def _set_minus(self):
        # Set x and y axis labels in Matplotlib to display '-' when negative.
        # If this setting is not enabled, 
        # negative signs will be displayed as triangles
        plt.rcParams['axes.unicode_minus'] = False