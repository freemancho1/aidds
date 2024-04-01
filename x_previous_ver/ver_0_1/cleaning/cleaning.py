import pandas as pd

import aidds.sys.config as cfg
from aidds.sys.utils import Logs, AiddsException
from aidds.module.data_io import get_provide_data, save_data


class Cleaning:
    def __init__(self): 
        self.logs = Logs('CLEANING') 
        self.cdict = {}
        try:
            self.data = get_provide_data()
            self._run()
        except Exception as e:
            raise AiddsException('CLEANING', se_msg=str(e))
        finally:
            self.logs.stop()
        
    def _run(self):
        # 공사비 데이터 학습대상 레코드 추출
        key = cfg.DATA_SETs[0]
        df = self.data[key]
        # (전주/전선 수를 제외한) 공사비 데이터 부분에서 학습 대상 레코드 조건
        # * 접수종류명(ACC_TYPE_NAME), 계약전력(CONT_CAP), 총공사비(TOTAL_CONS_COST)
        modeling_recs = \
            (df.ACC_TYPE_NAME  == cfg.CONSTRAINTs['ACC_TYPE_NAME']) & \
            (df.CONT_CAP        < cfg.CONSTRAINTs['MAX_CONT_CAP']) & \
            (df.CONS_COST < cfg.CONSTRAINTs['MAX_TOTAL_CONS_COST'])
            # (df.CONS_TYPE_CD   == cfg.CONSTRAINTs['CONS_TYPE_CD']) & \
        df = df[modeling_recs].reset_index(drop=True)
        
        # +++++++++++++++++++++++++++++++++++++++
        # 계약종별/공급방식 추가(나중에 계약종별이 있으니 제거해야 좋음)
        df.loc[:, 'CONT_TYPE'] = '1'
        df.loc[:, 'SUB_TYPE'] = '1'
        
        cons_df = df[cfg.COLs['PP'][key]['SOURCE']]
        self.cdict[key] = cons_df
        
        # 전주/전선/인입선 데이터 제약조건 처리
        # 공사비에 있는 공사번호별로 필요 컬럼만 남기고 정리
        for key in cfg.DATA_SETs[1:]:
            df = self.data[key]
            df = df[df[cfg.JOIN_COL].isin(cons_df[cfg.JOIN_COL])]
            self.cdict[key] = df[cfg.COLs['PP'][key]['SOURCE']]
            
        # 사업소명을 간단히 영문4자로 변경
        # 추후에는 사업소 코드를 받기 때문에 이 부분은 필요없음
        df = self.cdict['CONS'].copy()
        offc_list = df.OFFICE_NAME.unique().tolist()
        offc_cd = []
        for oname in df.OFFICE_NAME:
            offc_cd.append(f'{chr(ord("A")+offc_list.index(oname))*4}')
        df['OFFICE_CD'] = offc_cd
        self.cdict['CONS'] = df[cfg.COLs['PP']['CONS']['PP_IN']]
        
        # 전주 X, Y 좌표 만들기
        # 전주 X, Y 좌표는 모델링에서 사용하지 않기 때문에,
        # 이 부분은 모델링에서 제외
        # df = self.cdict['POLE'].copy()
        # df[['GEO_X', 'GEO_Y', 'T1', 'T2']] = \
        #     df.COORDINATE.str.split(',', expand=True)
        # self.cdict['POLE'] = df[cfg.COLs['PP']['POLE']['PP_IN']]
        self.cdict['POLE'] = self.cdict['POLE'][cfg.COLs['PP']['POLE']['PP_IN']]
        
        for key in cfg.DATA_SETs:
            save_data(self.cdict[key], f'CLEANING,BATCH,{key}')
            self.logs.mid(key, self.cdict[key].shape)
        