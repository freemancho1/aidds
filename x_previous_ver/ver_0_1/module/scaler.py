import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

import aidds.sys.config as cfg
from aidds.sys.utils import Logs, AiddsException
from aidds.module.data_io import save_data


class Scaling:
    def __init__(self, pp_df=None):
        self._logs = Logs('SCALING')
        try:
            self._pdf = pp_df
            self._ddf = {}              # 분리된 원본 데이터
            self.sdf = {}               # 스케일링된 데이터
            self._run()
        except AiddsException as ae:
            raise AiddsException('SCALING_INIT', se_msg=ae)
        except Exception as e:
            raise AiddsException('SCALING_INIT', se_msg=e)
        finally:
            self._logs.stop()
            
    def _run(self):
        try:
            self._split_Xy_and_pckey()
            for pckey in cfg.PC_TYPEs:
                self._split_train_test(pckey=pckey)
                self._scaling(pckey=pckey)
        except AiddsException as ae:
            raise AiddsException('SCALING_RUN', se_msg=ae)
        except Exception as e:
            raise AiddsException('SCALING_RUN', se_msg=e)