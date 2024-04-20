import json
import pandas as pd

import aidds.sys.config as cfg
from aidds.sys.utils.logs import service_logs as logs
from aidds.sys.utils.exception import AppException
from aidds.sys.utils.data_io import get_service_pickle


class Predict:
    """ Web service that predicts construction costs 

        * Singleton service
    """
    def __init__(self) -> None:
        try:
            self._pkl, self._scaler, self._model = get_service_pickle()
            logs(code='predict.main')
        except Exception as e:
            raise AppException(e)
        
    def run(self, in_json=None):
        try:
            pass
        except Exception as e:
            raise AppException(e)
