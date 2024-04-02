import json
import pandas as pd

import aidds.sys.config as cfg
from aidds.sys.utils.logs import service_logs as logs
from aidds.sys.utils.exception import AiddsException
from aidds.sys.utils.data_io import read_data
from aidds.serving.service.preprocessing import Preprocessing


class Predict:
    def __init__(self):
        try:
            # self._modeling_cols = read_data('DUMP,MODELING_COLS')
            # 스케일링 코딩 후 위 부분을 config의 LOAD_PICKLEs에 추가
            self._memory_pkl = {
                key: read_data(file_code=f'DUMP,PP,{key}') \
                    for key in cfg.FILE_NAMEs['DUMP']['PP'].keys()
            }
            # self._model = {
            #     pckey: read_data(f'DUMP,MODELS,{pckey},BEST') \
            #         for pckey in cfg.PC_TYPEs
            # }
            # self._scaler = {
            #     pckey: read_data(f'DUMP,SCALER,{pckey}') \
            #         for pckey in cfg.PC_TYPEs
            # }
            logs(mcode='PREDICT')
        except Exception as e:
            raise AiddsException(e)
        
    def run(self, input_json=None):
        try:
            input_json = input_json
            pp = Preprocessing(
                input_json=input_json, memory_pkl=self._memory_pkl
            )
            logs(value=pp.ret_json_dict)
            ret_json_dict = pp.ret_json_dict
            return ret_json_dict
        except Exception as e:
            raise AiddsException(e)