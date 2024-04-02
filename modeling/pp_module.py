import re
import pandas as pd

import aidds.sys.config as cfg
from aidds.sys.utils.exception import AiddsException


class PreprocessingModule:
    def cons(self, pdf=None):
        try:
            df = pdf
            
            # 결측치 처리
            df.fillna(0, inplace=True)
                
            # 일자정보 처리
            # * '최종변경일시'를 이용해 다양한 일자정보 컬럼 추가
            # * 참고로 일자정보가 날자형식이 아니면 날자형식으로 변환
            if df.ACC_DATE.dtype != '<M8[ns]':
                df.ACC_DATE = pd.to_datetime(df.ACC_DATE)
            df['YEAR'] = df.ACC_DATE.dt.year
            df['MONTH'] = df.ACC_DATE.dt.month
            df['DAY'] = df.ACC_DATE.dt.day
            df['DAYOFWEEK'] = df.ACC_DATE.dt.dayofweek
            df['DAYOFYEAR'] = df.ACC_DATE.dt.dayofyear
            df['YEAR_MONTH'] = df.ACC_DATE.dt.strftime("%Y%m").astype(int)
            
            df = df.drop(columns=['ACC_DATE'])
            
            return df
        except Exception as e:
            raise AiddsException(e)
    
    def calculate(self, soc_df=None, fdict=None):
        try:
            df = soc_df

            # 공사비까지 전처리된 데이터 셋에 설비 갯 수 컬럼 추가(3개)
            # 공사비 데이터 셋은 처리하지 않아도 됨
            for key in cfg.DATA_SETs[1:]:
                _df = fdict[key].copy()
                cons_ids_cnt = _df[cfg.JOIN_COL].value_counts()
                col_name = f'{key}_CNT'
                df = pd.merge(
                    df, cons_ids_cnt.rename(col_name),
                    left_on=cfg.JOIN_COL, right_on=cons_ids_cnt.index, how='left'
                )
                df[col_name] = df[col_name].fillna(0)
                
            # 모델 학습에 사용할 레코드 추출
            # * 전주/전선 갯 수가 10개 이상인 경우 
            # * 인입선 갯 수가 1개 인 경우 
            modeling_recs = \
                (df.POLE_CNT >= cfg.CONSTRAINTs['MIN_POLE_CNT']) & \
                (df.POLE_CNT <= cfg.CONSTRAINTs['MAX_POLE_CNT']) & \
                (df.LINE_CNT >= cfg.CONSTRAINTs['MIN_LINE_CNT']) & \
                (df.LINE_CNT <= cfg.CONSTRAINTs['MAX_LINE_CNT']) & \
                (df.SL_CNT   == cfg.CONSTRAINTs['SL_CNT'])
            df = df[modeling_recs].reset_index(drop=True)
            return df
        except Exception as e:
            raise AiddsException(e)
    
    def pole(self, sdf=None):
        try:
            df = sdf.copy()
            
            # 결측치 처리
            df.fillna(0, inplace=True)        
            
            # 코드형 컬럼 One-Hot Encoding
            prefix = ['POLE_SHAPE', 'POLE_TYPE', 'POLE_SPEC']
            cols = [x+'_CD' for x in prefix]
            # 숫자형 값 통일(실수형이 아닌 값을 실수형으로 변환)
            # (One-Hot Encoding시 동일한 컬럼값을 만들기 위해 실행)
            if df.POLE_SPEC_CD.dtype != 'float64':
                df['POLE_SPEC_CD'] = df['POLE_SPEC_CD'].astype(float)
            df = pd.get_dummies(df, columns=cols, prefix=prefix)
            # True, False값을 1, 0으로 변환
            df = df.apply(lambda x: int(x) if isinstance(x, bool) else x)
            
            return df
        except Exception as e:
            raise AiddsException(e)
    
    def line(self, sdf=None):
        try:
            df = sdf.copy()
            # 숫자형 값 통일(실수형이 아닌 값을 실수형으로 변환)
            # (One-Hot Encoding시 동일한 컬럼값을 만들기 위해 실행)
            if df.LINE_SPEC_CD.dtype != 'float64':
                df['LINE_SPEC_CD'] = df['LINE_SPEC_CD'].astype(float)
            if df.NEUTRAL_SPEC_CD.dtype != 'float64':
                df['NEUTRAL_SPEC_CD'] = df['NEUTRAL_SPEC_CD'].astype(float)   
            # 중성선규격코드(NEUTRAL_SPEC_CD)에 0.0과 NaN이 존재(NaN=>999.0 변환)
            df['NEUTRAL_SPEC_CD'] = df['NEUTRAL_SPEC_CD'].fillna(999.0)
            # 중성선종류코드(NEUTRAL_TYPE_CD)의 NaN값을 문자열 'NaN'으로 치환
            df.NEUTRAL_TYPE_CD = df.NEUTRAL_TYPE_CD.fillna('NaN')
            # 결선방식이 41인 값이 1개만 존재하기 때문에 많이 있는 43으로 치환
            df.WIRING_SCHEME = df.WIRING_SCHEME.replace(41, 43)
            # 전선 전체길이 추가: = 선로길이(SPAN) * 전선 갯 수(PHASE)
            df.loc[:, 'LINE_LENGTH'] = df.SPAN * df.LINE_PHASE_CD

            # 결측치 처리
            df.fillna(0, inplace=True)
            
            # 코드형 컬럼 One-Hot Encoding
            # WIRING_SCHEME은 마지막에 '_CD'가 붙지 않음
            prefix = ['WIRING_SCHEME', 'LINE_TYPE', 'LINE_SPEC', 'LINE_PHASE',
                    'NEUTRAL_TYPE', 'NEUTRAL_SPEC']
            columns = [x+'_CD' for x in prefix if x != 'WIRING_SCHEME']
            columns += ['WIRING_SCHEME']
            df = pd.get_dummies(df, columns=columns, prefix=prefix)
            # True, False를 1, 0으로 변환
            df = df.apply(lambda x: int(x) if isinstance(x, bool) else x)
            
            return df
        except Exception as e:
            raise AiddsException(e)
        
    
    def sl(self, sdf=None):
        try:
            df = sdf.copy()
            # 숫자형 값 통일(실수형이 아닌 값을 실수형으로 변환)
            # (One-Hot Encoding시 동일한 컬럼값을 만들기 위해 실행)
            if df.SL_SPEC_CD.dtype != 'float64':
                df['SL_SPEC_CD'] = df['SL_SPEC_CD'].astype(float)
            # 결측치 처리
            df.fillna(0, inplace=True)
            
            # 코드형 컬럼 One-Hot Encoding
            prefix = ['SL_TYPE', 'SL_SPEC']
            columns = [col+'_CD' for col in prefix]
            df = pd.get_dummies(df, columns=columns, prefix=prefix)
            df = df.apply(lambda x: int(x) if isinstance(x, bool) else x)
            
            return df
        except Exception as e:
            raise AiddsException(e)
    
    def calculate_sum(self, df, cols, pdf):
        try:
            unique_cons_ids = df[cfg.JOIN_COL].unique()
            cons_id_sums = []
            # 공사번호별 합산
            for cid in unique_cons_ids:
                cons_id_sums.append(
                    [cid]+df[df[cfg.JOIN_COL]==cid][cols].sum().values.tolist())
            # 공사번호별 설비정보 그룹 데이터
            sums_df = pd.DataFrame(cons_id_sums, columns=[cfg.JOIN_COL]+cols)
                
            # 모델링 데이터에 설비정보 그룹 데이터 병합
            _pdf = pd.merge(
                pdf, sums_df, left_on=cfg.JOIN_COL, right_on=cfg.JOIN_COL, how='left'
            )
            return _pdf
        except Exception as e:
            raise AiddsException(e)
        