import pandas as pd 

import aidds.sys.config as cfg
from aidds.sys.utils.logs import ModelingLogs as Logs
from aidds.sys.utils.exception import AiddsException
from aidds.sys.utils.data_io import get_provide_data, save_data


class Cleaning: 
    def __init__(self):
        try:
            self._logs = Logs('CLEANING')
            self._cd_dict = {}                  # cd_data: cleaning df dict
            self._pd_dict = get_provide_data()  # pd_data: provide df dict
            self._run()
        except (AiddsException, Exception) as e:
            raise AiddsException(e)
        finally:
            # Logs()에서 에러가 발생하면 self._logs 속성이 생성되지 않음
            if hasattr(self, '_logs'):
                self._logs.stop()
            
    def _run(self):
        try:
            # 공사비 데이터 학습대상 추출
            key = cfg.DATA_SETs[0]      # 'CONS'
            df = self._pd_dict[key]
            # (전주/전선 수를 제외한) 공사비 데이터 부분에서 학습 대상 레코드 조건
            # * 접수종류명(ACC_TYPE_NAME), 계약전력(CONT_CAP), 총공사비(TOTAL_CONS_COST)
            modeling_recs = \
                (df.ACC_TYPE_NAME  == cfg.CONSTRAINTs['ACC_TYPE_NAME']) & \
                (df.CONT_CAP        < cfg.CONSTRAINTs['MAX_CONT_CAP']) & \
                (df.CONS_COST       < cfg.CONSTRAINTs['MAX_TOTAL_CONS_COST'])
                # (df.CONS_TYPE_CD   == cfg.CONSTRAINTs['CONS_TYPE_CD']) & \
            df = df[modeling_recs].reset_index(drop=True)
            
            # +++++++++++++++++++++++++++++++++++++++
            # 계약종별/공급방식 추가(나중에 계약종별이 있으니 제거해야 좋음)
            df.loc[:, 'CONT_TYPE'] = '1'
            df.loc[:, 'SUB_TYPE'] = '1'
            
            # 사업소명을 간단히 영문4자로 변경
            # 추후에는 사업소 코드를 받기 때문에 이 부분은 필요없음
            office_names = df.OFFICE_NAME.unique().tolist()
            office_cds = []
            for oname in df.OFFICE_NAME:
                office_cds.append(f'{chr(ord("A")+office_names.index(oname))*4}')
            df['OFFICE_CD'] = office_cds
            self._cd_dict[key] = df[cfg.COLs['PP'][key]['PP_IN']]
            
            # 전주/전선/인입선 데이터 중 공사비의 공사번호가 없는 레코드 제거
            for key in cfg.DATA_SETs[1:]:
                df = self._pd_dict[key]
                df = df[df[cfg.JOIN_COL].isin(self._cd_dict['CONS'][cfg.JOIN_COL])]
                self._cd_dict[key] = df[cfg.COLs['PP'][key]['SOURCE']]
            # 전주데이터 GEO_X, GEO_Y 제거
            self._cd_dict['POLE'] = self._cd_dict['POLE'][cfg.COLs['PP']['POLE']['PP_IN']]
            
            # 크리닝 데이터 저장
            for key in cfg.DATA_SETs:
                save_data(self._cd_dict[key], f'CLEANING,BATCH,{key}')
                self._logs.mid(key, self._cd_dict[key].shape)

        except Exception as e:
            raise AiddsException(e)