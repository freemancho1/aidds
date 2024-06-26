import json
import numpy as np
import pandas as pd

import aidds_buy.sys.config as cfg
from aidds_buy.sys.utils.logs import service_logs as logs
from aidds_buy.sys.utils.exception import AiddsException
from aidds_buy.sys.utils.data_io import read_data

# 모델링에 구현되어 있는 전처리 공통 모듈
from aidds_buy.modeling.pp_module import PreprocessingModule as PPM


class Predict:
    def __init__(self):
        try:
            self._memory_pkl = {
                key: read_data(file_code=f'DUMP,PP,{key}') \
                    for key in cfg.FILE_NAMEs['DUMP']['PP'].keys() 
            }
            self._memory_pkl['MODELING_COLS'] = \
                read_data(file_code='DUMP,MODELING_COLS')
            self._model = {
                pc_key: read_data(f'DUMP,MODELS,{pc_key},BEST') \
                    for pc_key in cfg.PC_TYPEs
            }
            self._scaler = {
                pc_key: read_data(f'DUMP,SCALER,{pc_key}') \
                    for pc_key in cfg.PC_TYPEs
            }
            self._training_cols = read_data('DUMP,MODELING_COLS')
            logs(mcode='PREDICT')
        except Exception as e:
            raise AiddsException(e)
        
    def run(self, input_json=None): 
        try:
            input_json = input_json
            pp = Preprocessing(
                input_json=input_json, 
                memory_pkl=self._memory_pkl
            )
            sc = ScalingAndPrediction(
                pdf_dict=pp.pdf_dict, 
                models=self._model,
                scalers=self._scaler,
                memory_pkls=self._memory_pkl,
                training_cols=self._training_cols
            )
            pred_result_dict = sc.pred_result_dict
            # np.int64형 정수를 파이썬 기본 정수로 변환
            for main_key in pred_result_dict.keys():
                for sub_key in pred_result_dict[main_key]:
                    pred_result_dict[main_key][sub_key] = \
                        self._convert_to_builtin_type(
                            pred_result_dict[main_key][sub_key]
                        )
            return json.dumps(pred_result_dict)
        except Exception as e:
            raise AiddsException(e)
        
    def _convert_to_builtin_type(self, obj):
        return int(obj) if isinstance(obj, np.int64) else obj
        

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
            for pn_key in self._cd_dict.keys():
                # 공사비 데이터 전처리
                self._cons(pn_key=pn_key)
                # 설비(전주/전선/인입선) 데이터 전처리
                for key in cfg.DATA_SETs[1:]:
                    self._pp_facilities_data(key=key, pn_key=pn_key)
        except Exception as e:
            raise AiddsException(e)
        
    def _json_to_dfdict(self):
        # 요청된 JSON 데이터를 이용해 예측 입력용 데이터프레임과,
        # 예측된 값 리턴을 위한 리턴용 JSON 데이터를 만듬
        try:
            # 접수번호 및 접수번에의 예측 건수(추천 건수) 출력
            first_key = next(iter(self._input_json))
            acc_no = self._input_json[first_key]['CONS']['ACC_NO']
            value = f'ACC_NO={acc_no}, size={len(self._input_json)}'
            logs(mcode='INPUT_JSON_SIZE', value=value)
            
            self.ret_json_dict = self._input_json.copy()
            
            # 추천 번호별 처리
            for pn_key in self._input_json.keys():
                self._cd_dict[pn_key] = {}
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
                    self._cd_dict[pn_key][fc_key] = df
        except Exception as e:
            raise AiddsException(e)
        
    def _cons(self, key=None, pn_key=None):
        try:
            df = self._cd_dict[pn_key]['CONS']
            df = self._ppm.cons(df)
            
            # 사업소 코드를 이용해 사업소 번호를 변경
            offices = self._memory_pkl['OFFICE_CDS']
            office_idxs = []
            for oname in df.OFFICE_CD:
                office_idxs.append(offices.index(oname))
            df['OFFICE_NO'] = office_idxs
            df = df.drop(columns=['OFFICE_CD'])
            
            # 설비 갯 수 계산
            df = self._ppm.calculate(soc_df=df, fdict=self._cd_dict[pn_key])
            # 공사비 전처리 결과 저장
            self.pdf_dict[pn_key] = df
        except Exception as e:
            raise AiddsException(e)

    def _pp_facilities_data(self, key=None, pn_key=None):
        try:
            df = self._cd_dict[pn_key][key]
            df = eval(f'self._ppm.{key.lower()}(df)')
            
            # 모델링 작업에서 사용한 컬럼 정보를 이용해 서비스 데이터 컬럼 추가
            cols = self._memory_pkl[f'{key}_ONE_HOT_COLS']
            df_cols = df.columns.tolist()
            append_cols = [col for col in cols if col not in df_cols]
            df.loc[:, append_cols] = 0
            
            # 각 공사비별 설비 데이터 합계 계산
            sum_cols = df.columns.tolist()[1:]
            self.pdf_dict[pn_key] = \
                self._ppm.calculate_sum(df, sum_cols, self.pdf_dict[pn_key])
        except Exception as e:
            raise AiddsException(e)
        
    def _pp_to_scaler(self, pn_key=None):
        # 최종완료시점에서 NaN 처리
        # 서비스 시점에 전주나 인입선이 없는 공사일 경우 NaN값이 올 수 있음
        self.pdf_dict[pn_key].fillna(0, inplace=True)
        # 서비스 시점의 컬럼 순서를 모델링 시점의 컬럼 순서로 조정
        self.pdf_dict[pn_key] =\
            self.pdf_dict[pn_key].reindex(columns=self._memory_pkl['LAST_PP_COLS'])
        
    
class ScalingAndPrediction:
    def __init__(
        self, 
        pdf_dict=None, 
        models=None, 
        scalers=None,
        memory_pkls=None,
        training_cols=None
    ):
        try:
            self._pdf_dict = pdf_dict
            self._models = models
            self._scalers = scalers
            self._memory_pkls = memory_pkls
            self._training_cols = training_cols
            self.pred_result_dict = {}
            self._run()
        except Exception as e:
            raise AiddsException(e)
        
    def _run(self):
        try:
            for pn_key in self._pdf_dict.keys():
                pdf = self._pdf_dict[pn_key].copy()
                X = pdf[self._training_cols].reset_index(drop=True)
                logs(value=f'++++ len: {len(self._training_cols)}, {X.shape}')
                self.pred_result_dict[pn_key] = {
                    cfg.JOIN_COL: pdf.loc[0, cfg.JOIN_COL],
                    cfg.COLs['TARGET']: pdf.loc[0, cfg.COLs['TARGET']]
                }
                pc_key = X.loc[0, cfg.PC_COL].astype(int)
                scaler = self._scalers['1'] if pc_key==1 \
                    else self._scalers['N1']
                model = self._models['1'] if pc_key==1 \
                    else self._models['N1']
                scaled_X = scaler.transform(X)
                pred_y1 = model.predict(scaled_X)[0]
                pred_y2 = self._models['ALL'].predict(
                    self._scalers['ALL'].transform(X)
                )[0]
                self.pred_result_dict[pn_key].update({
                    'PRED1': pred_y1, 'PRED2': pred_y2
                })
        except Exception as e:
            raise AiddsException(e)