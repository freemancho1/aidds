import json 
import pandas as pd

import aidds.sys.config as cfg 
from aidds.sys.utils.logs import service_logs as logs
from aidds.sys.utils.exception import AiddsException
from aidds.sys.utils.data_io import get_service_pickle
from aidds.sys.utils.ect import convert_to_builtin_int
# 모델링 부분에 구현되어 있는 전처리 공통 모듈
from aidds.modeling.pp_module import PreprocessingModule


class Predict:
    # 서비스시 in_json 제거
    def __init__(self, in_json=None):
        try:
            self._pkl = get_service_pickle()
            self._ppm = PreprocessingModule()
            logs(code='predict.main')
            # 서비스시 제거
            self.run(in_json)
        except Exception as e:
            raise AiddsException(e)
        
    def run(self, in_json=None):
        try:
            # 이 함수에서 사용할 데이터는 init에서 선언된 데이터와 달리
            # run함수를 실행할 때 할당되는 데이터로 구성됨
            self._in_json = in_json     # Input JSON data
            self._cd_dict = {}          # Cleaning DataFrame Dictionary
            self._ppdf_dict = {}        # Preprocessing DataFrame Dictionary
            self._ret_json_dict = {}    # Return JSON data Dictionary
            # acc_no, cons_cost(실공사비), pred_all(전체예측), pred_pc(PC갯수별 예측)
            # 정보가 들어갈 딕셔너리
            self._pred_result_dict = {} 
            self._preprocessing()
            self._scaling_and_prediction()
            self._np_int64_to_python_int()
            # _pred_result_dict에 mape 추가해 로그 출력
            # ret_json_dict에 리턴할 값 추가
            # ret_json_dict에 리턴할 값 추가
            # ret_json_dict에 리턴할 값 추가
            # ret_json_dict에 리턴할 값 추가
            # ret_json_dict에 리턴할 값 추가
        except Exception as e:
            raise AiddsException(e)
        
    def _preprocessing(self):
        try:
            self._json_to_dataframe_dict()
            for pn_id in self._cd_dict.keys():
                # 공사비 데이터 전처리
                self._pp_cons(pn_id=pn_id)
                # 설비 데이터 전처리
                for pds_id in cfg.type.pds.ids[1:]:
                    self._pp_facilities_data(pds_id=pds_id, pn_id=pn_id)
                # 전처리 완료 처리
                # 최종 NaN처리 및 모델링 부분과 컬럼순서 일치시킴
                self._pp_to_scaler(pn_id=pn_id)
        except Exception as e:
            raise AiddsException(e)
        
    def _json_to_dataframe_dict(self):
        # 입력된 JSON 데이터를 이용해
        # 1. 예측에 사용할 데이터프레임과
        # 2. 예측 결과를 리턴할 JSON 데이터 딕셔너리를 만듬
        try:
            # in_json: 이 함수에서 사용한 temp data
            # 리턴값: 입력값 + 예측 공사비
            in_json = self._ret_json_dict = self._in_json.copy()
            # 가장 첫 번째 키값을 가져옴(리스트, 딕셔너리, JSON에서 다 사용 가능)
            first_key = next(iter(in_json))
            acc_no = in_json[first_key][cfg.type.pds.cons][cfg.col.join]
            # 요청된 접수번호의 추천경로 갯 수를 출력
            value = f'{cfg.col.join}={acc_no}, size={len(in_json)}'
            logs(code='predict.json_size', value=value)

            # 추천번호별로 JSON데이터를 예측에 사용할 데이터프레임으로 변환
            # pnid = predict number id
            for pn_id in in_json.keys():
                self._cd_dict[pn_id] = {}
                # 추천번호별 공사비와 설비(전주/전선/인입선) 처리
                for pds_id in cfg.type.pds.ids:
                    json_data = in_json[pn_id][pds_id]
                    # 공사비 데이터 예외처리
                    if pds_id == cfg.type.pds.cons:
                        # 데이터프레임으로 만들기 위해 차원 추가
                        df = pd.DataFrame([json_data])
                        # 예측에 필요하지 않은 pred_no/type 제거
                        df.drop(columns=['pred_no', 'pred_type'], inplace=True)
                        # 리턴용 JSON파일에 불필요 컬럼 제거
                        # 설비 데이터에는 제거할 항목 없음
                        # join, cons_cost, pred_no, pred_type 빼고 제거
                        for col in cfg.col.pp.cons.source.service[4:]:
                            self._ret_json_dict[pn_id][pds_id].pop(col, None)
                    else:
                        # 설비데이터를 배열로 변환
                        json_data = [value for _, value in json_data.items()]
                        df = pd.DataFrame(json_data)
                        # # 전주 데이터 예외처리(좌표정보 제거)
                        # if pds_id == cfg.type.pds.pole:
                        #     print(df.columns)
                        #     df.drop(columns=['geo_x', 'geo_y'], inplace=True)
                    # 추천번호별 설비정보 데이터프레임 저장
                    self._cd_dict[pn_id][pds_id] = df
        except Exception as e:
            raise AiddsException(e)

    def _pp_cons(self, pn_id=None):
        try:
            df = self._cd_dict[pn_id][cfg.type.pds.cons]
            # 공통모듈 전처리
            df = self._ppm.cons(cons_df=df)
            # 사업소코드를 이용해 사업소번호 생성
            office_idxs = []
            for oname in df.office_cd:
                office_idxs.append(self._pkl['pp.office.codes'].index(oname))
            df[cfg.col.base.office_id] = office_idxs
            
            # 설비 갯 수 계산
            df = self._ppm.calculate(pp_df=df, cd_dict=self._cd_dict[pn_id])
            # 공사비 전처리 결과 저장
            self._ppdf_dict[pn_id] = df
        except Exception as e:
            raise AiddsException(e)

    def _pp_facilities_data(self, pds_id=None, pn_id=None):
        try:
            df = self._cd_dict[pn_id][pds_id]
            # 설비별 전처리 공통모듈 전처리
            # 여기서 설비별 One-Hot Encoding을 수행함
            df = eval(f'self._ppm.{pds_id}(df)')
            
            # 모델링 부분에서 사용한 컬럼정보를 이용해 서비스 데이터 컬럼 추가
            cols = self._pkl[f'pp.one_hot_cols.{pds_id}']
            df_cols = df.columns.tolist()
            append_cols = [col for col in cols if col not in df_cols]
            df.loc[:, append_cols] = 0
            # 컬럼 순서는 나중에 일괄적으로 모델링 부분과 맞춰줌
            
            # 각 공사비별 설비 데이터 합산 계산
            sum_cols = df.columns.tolist()[1:]
            self._ppdf_dict[pn_id] = \
                self._ppm.summary(df=df, cols=sum_cols, ppdf=self._ppdf_dict[pn_id])
        except Exception as e:
            raise AiddsException(e)
        
    def _pp_to_scaler(self, pn_id=None):
        try:
            # 최종 완료시점에서 NaN 처리
            self._ppdf_dict[pn_id].fillna(0, inplace=True)
            # 서비스 부분의 컬럼 순서를 모델링 부분과 일치시킴
            self._ppdf_dict[pn_id] = \
                self._ppdf_dict[pn_id].reindex(columns=self._pkl['pp.last_cols'])
        except Exception as e:
            raise AiddsException(e)
        
    def _scaling_and_prediction(self):
        try:
            for pn_id in self._ppdf_dict.keys():
                ppdf = self._ppdf_dict[pn_id].copy()
                train_x = ppdf[self._pkl['modeling_cols']].reset_index(drop=True)
                self._pred_result_dict[pn_id] = {
                    # 접수번호
                    cfg.col.join: ppdf.loc[0, cfg.col.join],
                    # 실 공사비
                    cfg.col.target: ppdf.loc[0, cfg.col.target]
                }
                
                # 전체 모델링 모델로 결과 예측                
                scaler_all = self._pkl['scaler.all'] 
                model_all = self._pkl['models.all.best']
                scaled_x_all = scaler_all.transform(train_x)
                pred_all = model_all.predict(scaled_x_all)[0]
                # 전주 갯 수별 모델링 모델로 결과 예측
                # 전주 갯 수 읽어오기
                pc_cnt = train_x.loc[0, cfg.col.pc].astype(int)
                scaler_pc = self._pkl['scaler.e1'] if pc_cnt == 1 \
                    else self._pkl['scaler.n1']
                model_pc = self._pkl['models.e1.best'] if pc_cnt == 1 \
                    else self._pkl['models.n1.best']
                scaled_x_pc = scaler_pc.transform(train_x)
                pred_pc = model_pc.predict(scaled_x_pc)[0]
                
                # 예측결과 저장
                self._pred_result_dict[pn_id].update({
                    'pred_all': pred_all, 'pred_pc': pred_pc
                })
        except Exception as e:
            raise AiddsException(e)
        
    def _np_int64_to_python_int(self):
        try:
            for pn_id in self._pred_result_dict.keys():
                for key in self._pred_result_dict[pn_id].keys():
                    self._pred_result_dict[pn_id][key] = \
                        convert_to_builtin_int(self._pred_result_dict[pn_id][key])
        except Exception as e:
            raise AiddsException(e)
        
        