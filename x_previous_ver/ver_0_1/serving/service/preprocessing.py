import pandas as pd
import aidds_buy.sys.config as cfg
from aidds_buy.sys.utils import AiddsServiceException as ASE
from aidds_buy.module.pp_mod import PreprocessingModule

class Preprocessing:
    def __init__(self, jdict=None, pkl=None):
        try:
            # Cleaning Data
            self._cdict = None
            self._jdict = jdict
            self._pkl = pkl
            # Preprocessing Data
            self.pdict = {}
            self.rdict = None
            self.pp = PreprocessingModule()
            self._run()
        except ASE as ae:
            raise ASE(emsg='[PP][INIT]', smsg=ae)
        except Exception as e:
            raise ASE(emsg='[PP][INIT] ', smsg=e) 
            
    def _run(self):
        try:
            self._cdict, self.rdict = self._json_to_dfdict()
            for pn_key in self._cdict.keys():
                self.pdict[pn_key] = self._cons(key='CONS', pn_key=pn_key)
                for key in cfg.DATA_SETs[1:]:
                    self._pp_facilitie_data(key, pn_key=pn_key)
                self._pp_to_scaler(pn_key=pn_key)
        except ASE as ae:
            raise ASE(emsg='[RUN]', smsg=ae)
        except Exception as e:
            raise ASE(emsg='[RUN] ', smsg=e)
        
    def _json_to_dfdict(self):
        try:
            jdict = self._jdict
            df_dict = {}            # 예측용 데이터프레임 딕셔너리
            r_dict = jdict.copy()   # 리턴용 JSON 딕셔너리
            for pn_key in jdict.keys():
                df_dict[pn_key] = {}
                for fc_key in  jdict[pn_key].keys():
                    _sdata = jdict[pn_key][fc_key]
                    if fc_key == 'CONS':
                        _data = [_sdata]
                        df = pd.DataFrame(_data)
                        df.drop(columns=['PRED_NO', 'PRED_TYPE'], inplace=True)
                        # 리턴용 JSON에 필요한 컬럼 이외는 제외
                        # 전주/전선/인입선에는 뺄게 없음
                        for col in cfg.COLs['PP']['CONS']['PRED'][4:]:
                            r_dict[pn_key]['CONS'].pop(col, None)
                    else:
                        _data = [v for _, v in _sdata.items()]
                        df = pd.DataFrame(_data)
                        if fc_key == 'POLE':
                            df.drop(columns=['GEO_X', 'GEO_Y'], inplace=True)
                    df_dict[pn_key][fc_key] = df
            return df_dict, r_dict
        except ASE as ae:
            raise ASE(emsg='[JSON_TO_DFDICT]', smsg=ae)
        except Exception as e:
            raise ASE(emsg='[JSON_TO_DFDICT] ', smsg=e)
        
    def _cons(self, key=None, pn_key=None):
        try:
            df = self._cdict[pn_key][key]
            df = self.pp.cons(df)
            
            office_list = self._pkl['OFFICE_LIST']
            # 사업소 코드를 이용해 사업소 번호로 변경
            office_idxs = []
            for oname in df.OFFICE_CD:
                office_idxs.append(office_list.index(oname))
            df['OFFICE_NO'] = office_idxs
            df = df.drop(columns=['OFFICE_CD'])
            
            # 설비 갯 수 계산 
            df = self._calculate(df, pn_key=pn_key)
            return df
        except ASE as ae:
            raise ASE(emsg='[CONS]', smsg=ae)
        except Exception as e:
            raise ASE(emsg='[CONS] ', smsg=e)
    
    def _calculate(self, sdf=None, pn_key=None):
        try:
            df = self.pp.calculate(sdf, self._cdict[pn_key])
            return df
        except ASE as ae:
            raise ASE(emsg='[CALCULATE]', smsg=ae)
        except Exception as e:
            raise ASE(emsg='[CALCULATE] ', smsg=e)
    
    def _pp_facilitie_data(self, key=None, pn_key=None):
        try:
            df = self._cdict[pn_key][key]
            df = eval(f'self.pp.{key.lower()}(df)')
            # 실시간 처리에서 동일 컬럼을 추가하기 위해 학습에서 나온 컬럼 리스트 저장
            cols = self._pkl[f'{key}_ONE_HOT_COLS']
            df_cols = df.columns.tolist()
            append_cols = [x for x in cols if x not in df_cols]
            df.loc[:, append_cols] = 0
            
            sum_cols = df.columns.tolist()[1:]
            self.pdict[pn_key] = self.pp.calculate_sum(df, sum_cols, self.pdict[pn_key])
        except ASE as ae:
            raise ASE(emsg=f'[FD_{key}]', smsg=ae)
        except Exception as e:
            raise ASE(emsg=f'[FD_{key}] ', smsg=e)
            
    def _pp_to_scaler(self, pn_key=None):
        # 최종 완료시점에서 NaN값을 0으로 처리
        # 온라인 작업 시 인입선이 없거나 전주가 없는 작업 등에서 NaN가 올 수 있음
        self.pdict[pn_key].fillna(0, inplace=True)
        # 모델링 시점의 컬럼 순서를 읽어와 서비스 데이터프레임의 컬럼 순서 조점
        self.pdict[pn_key] = \
            self.pdict[pn_key].reindex(columns=self._pkl['LAST_PP_COLS'])
    