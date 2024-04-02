import pandas as pd

import aidds.sys.config as cfg 
from aidds.sys.utils.logs import service_logs as logs
from aidds.sys.utils.exception import AiddsException

# 모델링에 구현되어 있는 전처리 공통 모듈
from aidds.modeling.pp_module import PreprocessingModule as PPM


class Preprocessing:
    def __init__(self, input_json=None, memory_pkl=None):
        try:
            self._input_json = input_json
            self._memory_pkl = memory_pkl
            self._ppm = PPM()
            self._cd_dict = {}          # Cleaning DataFrame Dictionary
            self.pdf_dict = {}          # Preprocessing DataFrame Dictionary
            self.ret_json_dict = {}     # Return JSON Dictionary
            self._run()
        except Exception as e:
            raise AiddsException(e)
        
    def _run(self):
        try:
            self._json_to_dfdict()
        except Exception as e:
            raise AiddsException(e)
        
    def _json_to_dfdict(self):
        # 요청된 JSON 데이터를 이용해 예측 입력용 데이터프레임과,
        # 예측된 값 리턴을 위한 리턴용 JSON 데이터를 만듬
        try:
            # 접수번호 및 접수번에의 예측 건수(추천 건수) 출력
            first_key = next(iter(self._input_json))
            acc_no = self._input_json[first_key]['CONS']['ACC_NO']
            value = f'ACC_NO={acc_no}, size[{len(self._input_json)}]'
            logs(mcode='INPUT_JSON_SIZE', value=value)
            
            self.ret_json_dict = self._input_json.copy()
            
            # 추천 번호별 처리
            for pn_key in self._input_json.keys():
                self.pdf_dict[pn_key] = {}
                # 추천 번호별 공사비와 설비(전주/전선/인입선) 처리
                for fc_key in self._input_json[pn_key].keys():
                    json_data = self._input_json[pn_key][fc_key]
                    if fc_key == 'CONS':
                        json_data = [json_data]
                        df = pd.DataFrame(json_data)
                        df.drop(columns=['PRED_NO', 'PRED_TYPE'], inplace=True)
                        # 리턴용 JSON파일에 불필요 컬럼 제거
                        # 설비(전주/전선/인입선) 데이터에는 제거할 컬럼이 없음
                        for col in cfg.COLs['PP']['CONS']['PRED'][4:]:
                            self.ret_json_dict[pn_key]['CONS'].pop(col, None)
                    else:
                        json_datas = [value for _, value in json_data.items()]
                        df = pd.DataFrame(json_datas)
                        if fc_key == 'POLE':
                            df.drop(columns=['GEO_X', 'GEO_Y'], inplace=True)
                    self.pdf_dict[pn_key][fc_key] = df
        except Exception as e:
            raise AiddsException(e)