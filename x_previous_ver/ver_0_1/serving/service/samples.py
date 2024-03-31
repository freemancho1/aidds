import json
import random
import pandas as pd

import aidds.sys.config as cfg
import aidds.sys.messages as msg
from aidds.sys.utils import AiddsServiceException as ASE
from aidds.sys.utils import ServiceLogs as Logs
from aidds.module.data_io import read_data, get_cleaning_data


class Samples:
    def __init__(self):
        self.target_df = read_data('PP_LAST')
        self.cdict = get_cleaning_data()
        self.logs = Logs(code='SAMPLE') 
        
    def get(self, sample_cnt=3):
        try:
            sample_key = random.sample(
                self.target_df[cfg.JOIN_COL].tolist(), k=sample_cnt)
            sample_dict = {}
            for key in sample_key:
                sub_dict = {}
                for fc_key in self.cdict.keys():
                    df = self.cdict[fc_key]
                    df = df[df[cfg.JOIN_COL]==key].copy()
                    sub_dict[fc_key] = df
                sample_dict[key] = sub_dict
            sample_json = self._sample_to_json(sample_dict)
            self.logs.mid(value=f'key={sample_key}')
            return sample_json
        except ASE as ae:
            raise ASE(emsg='[SAMPLE][GET]', smsg=ae)
        except Exception as e:
            raise ASE(emsg='[SAMPLE][GET] ', smsg=e)
        
    def _sample_to_json(self, s_dict=None):
        try:
            json_dict = {}
            acc_no = None
            pred_no = 1
            for idx, row in s_dict.items():
                pred_key = f'PRED_{pred_no}'
                json_dict[pred_key] = {}
                # 서로 다른 cons_id값을 가장 먼저 온 cons_id값으로 통일
                if acc_no is None:
                    acc_no = idx
                json_dict[pred_key]['CONS'] = row['CONS'].to_dict(orient='records')[0]
                json_dict[pred_key]['CONS'].update({
                    'ACC_NO': acc_no, 'PRED_NO': pred_no, 'PRED_TYPE': pred_no
                })
                json_dict[pred_key].update({'POLE': {}, 'LINE': {}, 'SL': {}})
                
                for key in cfg.DATA_SETs[1:]:
                    df = row[key]
                    # df = df.drop(columns=[cfg.JOIN_COL])
                    if key == 'POLE':
                        # 나중에 값을 받을 예정이고, X, Y값을 모델링에서
                        # 사용하지 않기 때문에 임의 텍스트 추가
                        df.loc[:, ['GEO_X', 'GEO_Y']] = 'GEO'
                        # df[['GEO_X', 'GEO_Y', 'TEMP1', 'TEMP2']] = \
                        #     df.COORDINATE.str.split(',', expand=True)
                        # df = df.drop(columns=([
                        #     'TEMP1', 'TEMP2', 'COORDINATE'
                        # ]))
                    fc_dict = {}
                    idx = 1
                    for _, sub_row in df.iterrows():
                        fc_dict[f'{key}_{idx}'] = sub_row.to_dict()
                        fc_dict[f'{key}_{idx}']['ACC_NO'] = acc_no
                        idx += 1
                    json_dict[pred_key][key] = fc_dict
                
                pred_no += 1
                
            sample_json = json.dumps(json_dict, ensure_ascii=False)
            return sample_json
        except Exception as e:
            raise ASE(emsg='[SAMPLE_TO_JSON] ', smsg=e)
                
        