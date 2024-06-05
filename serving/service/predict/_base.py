import json
import pandas as pd

from aidds_buy.sys import config as cfg 
from aidds_buy.sys.utils import service_logs as logs
from aidds_buy.sys.utils import app_exception
from aidds_buy.sys.utils import get_service_pickle
from aidds_buy.sys.utils import calculate_mape
from aidds_buy.serving import preprocessing


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
            raise app_exception(e)
        
    def run(self, in_json=None) -> json:
        try:
            pp = preprocessing(in_json=in_json, pkl=self._pkl)
            self._return_json = pp.return_json
            self._ppdf = pp.ppdf
            # Data for log display
            self._display_result = {}
            self._scaling_and_prediction()
            self._log_display()
            return json.dumps(self._return_json)
        except Exception as e:
            raise app_exception(e)
        
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
                    'pred': int(p), 'mape': round(calculate_mape(y, p), 3)
                })
                self._return_json[pnid]['cons']\
                    .update({cfg.cols.target: int(p)})
        except Exception as e:
            raise app_exception(e)

    def _log_display(self):
        try:
            logs(code='predict.result')
            for key in self._display_result.keys():
                p = self._display_result[key]
                value = f'{key} -> acc_no: {p["acc_no"]}, ' \
                        f'real: {p["cons_cost"]:>10,d}, ' \
                        f'pred: {p["pred"]:>10,d}, mape: {p["mape"]:>6.3f}'
                logs(value=value)
        except Exception as e:
            raise app_exception(e)