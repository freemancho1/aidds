import re
import pandas as pd

import aidds.sys.config as cfg
from aidds.sys.utils.exception import AiddsException


class PreprocessingModule:
    """ 데이터 전처리(모델링과 서비스에서 공통 사용) 모듈 """
    
    def cons(self, cons_df=None) -> pd.DataFrame:
        """ 공사비 전처리 공통 모듈 """
        try:
            df = cons_df.copy()
            # 결측치 처리
            df.fillna(0, inplace=True)
            
            # 공사일자를 기준으로 처리하는 부분을 추가하고 했는데,
            # 우리가 받은 데이터에는 접수일은 있어도 공사일은 없기 때문에
            # 공사일자 처리는 제외함
            
            # 추후에 추가할 내용이 있을 수 있기 때문에 남겨둠
            
            return df            
        except Exception as e:
            raise AiddsException(e)
        
    def calculate(self, pp_df=None, cd_dict=None) -> pd.DataFrame:
        """ 설비 갯 수 계산 공통 모듈 """
        try:
            ppdf = pp_df
            
            # 전처리된 공사비 데이터에 설비별 갯 수 추가
            for id in cfg.type.pds.ids[1:]:
                df = cd_dict[id].copy()
                # 'acc_no(cfg.col.join)'별 갯 수 계산
                cons_ids_cnt = df[cfg.col.join].value_counts()
                col_name = f'{id}_cnt'
                ppdf = pd.merge(
                    ppdf, cons_ids_cnt.rename(col_name),
                    left_on=cfg.col.join, right_on=cons_ids_cnt.index, how='left'
                )
                ppdf[col_name] = ppdf[col_name].fillna(0)
                
            # 설비 갯 수에 따른 제약조건 처리
            # - 전주/전선 10개 이하
            # - 인입선 갯 수 1개
            modeling_rows = \
                (ppdf.pole_cnt >= cfg.constraint.min_pole_cnt) & \
                (ppdf.pole_cnt <= cfg.constraint.max_pole_cnt) & \
                (ppdf.line_cnt >= cfg.constraint.min_line_cnt) & \
                (ppdf.line_cnt <= cfg.constraint.max_line_cnt) & \
                (ppdf.sl_cnt   == cfg.constraint.sl_cnt)
            ppdf = ppdf[modeling_rows].reset_index(drop=True)
            return ppdf
        except Exception as e:
            raise AiddsException(e)
        
    def pole(self, pole_df=None) -> pd.DataFrame:
        """ 전주 전처리 공통 모듈 """
        try:
            df = pole_df.copy()
            # 결측치 처리
            df.fillna(0, inplace=True)
            
            # 코드형 컬럼 One-hot Encoding
            cols = [
                cfg.col.base.pole_shape_cd,
                cfg.col.base.pole_type_cd,
                cfg.col.base.pole_spec_cd,
            ]
            prefix = [item[:-3] for item in cols]
            # 숫자형 값 통일(실수형이 아닌 값을 실수형으로 변환)
            # 1과 1.0이 서로 다른 OneHotEncoding의 결과 컬럼으로 생성됨
            if df.pole_spec_cd.dtype != 'float64':
                df.pole_spec_cd = df.pole_spec_cd.astype(float)
            # One-Hot Encoding
            df = pd.get_dummies(df, columns=cols, prefix=prefix)
            # True, False를 1과 0으로 변환
            df = df.apply(lambda item: int(item) if isinstance(item, bool) else item)
            return df
        except Exception as e:
            raise AiddsException(e)
        
    def line(self, line_df=None) -> pd.DataFrame:
        """ 전선 전처리 공통 모듈 """
        try:
            df = line_df.copy()
            
            # 코드형 컬럼 One-Hot Encoding을 위한 전처리
            ## OHE를 위해 숫자형 컬럼을 실수형으로 변환
            ## 1과 1.0이 서로 다른 OneHotEncoding의 결과 컬럼으로 생성됨
            if df.line_spec_cd.dtype != 'float64':
                df.line_spec_cd = df.line_spec_cd.astype(float)
            # 중성선 규격코드에 0.0과 NaN이 존재
            # - 구분하기 위해 NaN을 999.0으로 치환
            df.neutral_spec_cd = df.neutral_spec_cd.fillna(999.0)
            if df.neutral_spec_cd.dtype != 'float64':
                df.neutral_spec_cd = df.neutral_spec_cd.astype(float)
            # 중성선종류코드(neutral_type_cd)의 NaN값을 문자열 'NaN'으로 변환
            df.neutral_type_cd = df.neutral_type_cd.fillna('NaN')
            # 결선방식이 41인 값이 1개만 존재하기 때문에 많이 있는 43으로 치환
            df.wiring_scheme = df.wiring_scheme.replace(41, 43)
            # 전선 전체길이 추가 = 선로길이(SPAN) * 전선 갯 수(PHASE)
            df.loc[:, 'line_length'] = df.span * df.line_phase_cd
            
            # 기타 결측치 처리
            df.fillna(0, inplace=True)
            
            # One-Hot Encoding
            cols = [
                cfg.col.base.wiring_scheme,
                cfg.col.base.line_type_cd,
                cfg.col.base.line_spec_cd,
                cfg.col.base.line_phase_cd,
                cfg.col.base.neutral_type_cd,
                cfg.col.base.neutral_spec_cd
            ]
            # 'wiring_scheme'는 뒤에 '_cd'가 없으니 제외
            prefix = [cols[0]] + [item[:-3] for item in cols[1:]]
            df = pd.get_dummies(df, columns=cols, prefix=prefix)
            # True, False를 1, 0으로 변환
            df = df.apply(lambda item: int(item) if isinstance(item, bool) else item)
            
            return df
        except Exception as e:
            raise AiddsException(e)    
    
    def sl(self, sl_df=None) -> pd.DataFrame:
        """ 인입선 전처리 공통 모듈 """
        try:
            df = sl_df.copy()
            # 결측치 처리
            df = df.fillna(0)
            # 숫자형 데이터 실수로 변환
            if df.sl_spec_cd.dtype != 'float64':
                df.sl_spec_cd = df.sl_spec_cd.astype(float)
            # One-Hot Encoding
            cols = [
                cfg.col.base.sl_type_cd,
                cfg.col.base.sl_spec_cd,
            ]
            prefix = [item[:-3] for item in cols]
            df = pd.get_dummies(df, columns=cols, prefix=prefix)
            df = df.apply(lambda item: int(item) if isinstance(item, bool) else item)
            
            # 길이 컬럼 추가
            df.loc[:, 'sl_length'] = df.sl_span * df.sl_phase
            return df
        except Exception as e:
            raise AiddsException(e)
        
    def summary(self, df=None, cols=None, ppdf=None) -> pd.DataFrame:
        """ 각 설비별 One-Hot Encoding된 컬럼의 갯 수 계산(합계) """
        try:
            unique_cons_ids = df[cfg.col.join].unique()
            cons_id_sums = []
            # 공사번호별 합산
            for id in unique_cons_ids:
                append_value = df[df[cfg.col.join]==id][cols].sum().values.tolist()
                cons_id_sums.append([id] + append_value)
            # 공사번호 기준 합산 데이터 데이터프레임 생성
            sums_df = pd.DataFrame(cons_id_sums, columns=[cfg.col.join]+cols)
            # 합산 데이터프레임 전처리 데이터프레임에 병합
            _ppdf = pd.merge(ppdf, sums_df, on=cfg.col.join, how='left')
            return _ppdf
        except Exception as e:
            raise AiddsException(e)
        
        