import aidds.sys.config as cfg 
from aidds.sys.utils.logs import ModelingLogs as Logs
from aidds.sys.utils.data_io import save_data
from aidds.sys.utils.exception import AiddsException
from aidds.sys.utils.evaluations import regression_evals


class Learning:
    def __init__(self, scaling_data=None):
        try:
            self._logs = Logs('LEARNING')
            self._sdata = scaling_data
            self._best = {
                pc_key: {'MODEL': None, 'SCORE': 0, 'MODEL_KEY': ''} \
                    for pc_key in cfg.PC_TYPEs
            }
            self._history = {}
            self._run()
        except Exception as e:
            raise AiddsException(e)
        finally:
            if hasattr(self, '_logs'): self._logs.stop()
            
    def _run(self):
        try:
            pass
        except Exception as e:
            raise AiddsException(e)
        