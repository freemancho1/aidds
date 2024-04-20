import json
import pandas as pd

import aidds.sys.config as cfg
from aidds.sys.utils.logs import service_logs as logs
from aidds.sys.utils.exception import AppException
from aidds.sys.utils.data_io import get_service_pickle
from aidds.sys.utils.evaluation import calculate_mape
from aidds.serving.service.predict.preprocessing import PredictPreprocessing


class Predict:
    """ Web service that predicts construction costs 

        * Singleton service
    """
    def __init__(self) -> None:
        try:
            self._pkl, self._scaler, self._model = get_service_pickle()
            self._modeling_cols = self._pkl['modeling_cols']
            logs(code='predict.main')
        except Exception as e:
            raise AppException(e)
        
    def run(self, in_json=None) -> json:
        try:
            pp = PredictPreprocessing(in_json=in_json, pkl=self._pkl)
            self._return_json = pp.return_json
            self._ppdf = pp.ppdf
            # Data for log display
            self._display_result = {}
            self._scaling_and_prediction()
            logs(code='predict.result')
            if cfg.sys.cond.display_logs.service:
                for key in self._display_result.keys():
                    print(f'{key}: {self._display_result[key]}')
            return json.dumps(self._return_json)
        except Exception as e:
            raise AppException(e)
        
    def _scaling_and_prediction(self):
        try:
            for pnid in self._ppdf.keys():
                ppdf = self._ppdf[pnid].copy()
                self._display_result[pnid] = {
                    cfg.cols.join: ppdf.loc[0, cfg.cols.join],
                    cfg.cols.target: ppdf.loc[0, cfg.cols.target],
                }
                
                # Split x, y
                y = ppdf.pop(cfg.cols.target)[0]
                x = ppdf
                x[self._modeling_cols] = \
                    self._scaler.transform(x[self._modeling_cols])
                p = self._model.predict(x[self._modeling_cols])[0]
                
                # Save result
                self._display_result[pnid].update({
                    'pred': int(p), 'mape': round(calculate_mape(y=y, p=p),3)
                })
                self._return_json[pnid]['cons']\
                    .update({cfg.cols.target: int(p)})
        except Exception as e:
            raise AppException(e)
