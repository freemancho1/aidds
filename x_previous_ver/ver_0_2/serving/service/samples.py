import json
import random
import pandas as pd 

import aidds_buy.sys.config as cfg
import aidds_buy.sys.messages as msg

from aidds_buy.sys.utils.exception import AiddsException
from aidds_buy.sys.utils.logs import service_logs as logs
from aidds_buy.sys.utils.data_io import read_data, get_cleaning_data


class Samples:
    def __init__(self):
        try:
            self._source_df = read_data('PP_LAST')
            self._cd_dict = get_cleaning_data()
            logs(mcode='SAMPLE')
        except Exception as e:
            raise AiddsException(e)
        
    def get(self, sample_count=3):
        try:
            # 모델링 대상 데이터를 이용해 sample_count 만큼의
            # 샘플 데이터의 key(cfg.JOIN_COL)를 추출
            sample_keys = random.sample(
                self._source_df[cfg.JOIN_COL].tolist(), 
                k=sample_count
            )
            logs(value=f'sample_keys={sample_keys}')
            
            # 샘플 데이터 생성
            samples_dict = {}
            for key in sample_keys:
                sub_dict = {}
                for fc_key in self._cd_dict.keys():
                    df = self._cd_dict[fc_key]
                    df = df[df[cfg.JOIN_COL] == key]
                    sub_dict[fc_key] = df
                samples_dict[key] = sub_dict
            
            # 추출된 샘플을 JSON 데이터로 변환
            # 하나의 접수번호키로 통합된 3개의 접수번호 데이터
            return self._sample_to_json(samples=samples_dict)
        except Exception as e: 
            raise AiddsException(e)
        
    def _sample_to_json(self, samples=None):
        try:
            json_dict = {}
            samples_dict = samples
            acc_no = None
            pred_no = 1
            for idx, row in samples_dict.items():
                pred_key = f'PRED_{pred_no}'
                json_dict[pred_key] = {}
                # 각각의 접수번호를 가장 처음온 접수번호로 변경(접수번호 통일)
                if acc_no is None: acc_no = idx
                
                # 각 추천번호별 공사비정보 변경
                json_dict[pred_key]['CONS'] = \
                    row['CONS'].to_dict(orient='records')[0]
                json_dict[pred_key]['CONS'].update({
                    'ACC_NO': acc_no, 'PRED_NO': pred_no, 'PRED_TYPE': pred_no
                })
                
                # 각 추천번호별 설비(전주/전선/인입선)정보 추가
                json_dict[pred_key].update({'POLE': {}, 'LINE': {}, 'SL': {}})
                for key in cfg.DATA_SETs[1:]:
                    df = row[key].copy()
                    if key == 'POLE': 
                        df.loc[:,['GEO_X','GEO_Y']] = 'GEO'
                    # 각 추천번호별 설비정보 추출
                    fc_dict = {}
                    fc_seq = 1
                    for _, sub_row in df.iterrows():
                        fc_dict[f'{key}_{fc_seq}'] = sub_row.to_dict()
                        # 각 설비의 접수번호를 최초 접수번호로 변경
                        fc_dict[f'{key}_{fc_seq}']['ACC_NO'] = acc_no
                        fc_seq += 1
                    json_dict[pred_key][key] = fc_dict
                pred_no += 1
            
            samples_json = json.dumps(json_dict, ensure_ascii=False)
            return samples_json
        except Exception as e:
            raise AiddsException(e)