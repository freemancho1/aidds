import json
import pandas as pd
from typing import Type

import aidds.sys.config as cfg 
from aidds.sys.utils.logs import service_logs as logs
from aidds.sys.utils.exception import AppException
from aidds.modeling.preprocess_module import PreprocessModule as ppm


class PredictPreprocessing:
    def __init__(self, in_json=None, pkl=None) -> Type['PredictPreprocessing']:
        try:
            self._in_json = in_json
            self._pkl = pkl
            self._cleaning_df = {}
            # Preprocessing Datafram dict(Generate as many recommended counts)
            self.ppdf = {}
            # Return JSON data dict(Generate as many recommended counts)
            self.return_json = {}
            self._run()
        except Exception as e:
            raise AppException(e)
    
    def _run(self) -> None:
        try:
            self._json_to_dataframe()
        except Exception as e:
            raise AppException(e)
    
    def _json_to_dataframe(self) -> None:
        # Using the input JSON data dictionary
        # 1. Create a dataframe dictionary to be used for prediction
        # 2. Create a JSON data dictionary to return prediction results.
        try:
            # 'in_json': Temp data used in this function
            # 'self.return_json': in_json + predicted cost(added later)
            in_json = self.return_json = self._in_json.copy()
            # Get the first acc_no value 
            # (can be used in lists, dictionaries, and JSON)
            first_key = next(iter(in_json))
            acc_no = in_json[first_key][cfg.type.pds[0]][cfg.cols.join]
            
        except Exception as e:
            raise AppException(e)
    
    
        