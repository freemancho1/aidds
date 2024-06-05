import json
import inspect
import pandas as pd

import aidds_buy.sys.config as cfg
from aidds_buy.sys.utils import ServiceLogs as Logs
from aidds_buy.sys.utils import AiddsServiceException as ASE
from aidds_buy.module.data_io import read_data
from aidds_buy.serving.service.preprocessing import Preprocessing

class Predict:
    def __init__(self):
        # self._modeling_cols = read_data('DUMP,MODELING_COLS')
        # 스케일링 코딩 후 위 부분을 config의 LOAD_PICKLEs에 추가
        self._pkl = {
            name: read_data(fcode=f'DUMP,{name}') \
                for name in cfg.LOAD_PICKLEs
        }
        # self._model = {
        #     pckey: read_data(f'DUMP,MODELS,{pckey},BEST') \
        #         for pckey in cfg.PC_TYPEs
        # }
        # self._scaler = {
        #     pckey: read_data(f'DUMP,SCALER,{pckey}') \
        #         for pckey in cfg.PC_TYPEs
        # }
        self._logs = Logs('PREDICT')
        print(f'1__name__ = {__name__}')
        print(f'1____ = {inspect.currentframe().f_code.co_name}')
        
    def run(self, json_dict=None):
        try:
            print(f'2__name__ = {__name__}')
            print(f'2____ = {inspect.currentframe().f_code.co_name}')
            jdict = json_dict
            pp = Preprocessing(jdict=json_dict, pkl=self._pkl)
            for pn_key in pp.pdict.keys():
                pass
            
            return pp.rdict
        except ASE as ae:
            raise ASE(emsg='[PREDICT][RUN]', smsg=ae)
        except Exception as e:
            raise ASE(emsg='[PREDICT][RUN] ', smsg=e)
    
    

