import pandas as pd

import aidds_buy.sys.config as cfg
import aidds_buy.sys.message as msg
from aidds_buy.sys.utils.logs import ModelingLogs as Logs
from aidds_buy.sys.utils.exception import AiddsException
from aidds_buy.sys.utils.data_io import get_provide_data, save_data


class Cleaning:
    def __init__(self): 
        try:
            self._logs = Logs(code='cleaning')
            self.cd_dict = {}
            self._pd_dict = get_provide_data()
            self._run()
        except Exception as e:
            raise AiddsException(e)
        finally:
            if hasattr(self, '_logs'): self._logs.stop()
            
    def _run(self):
        try:
            # 공사비 데이터 학습대상 추출
            id = cfg.type.pds.cons
            df = self._pd_dict[id]
            
            # (전주/전선 수를 제외한) 공사비 데이터 부분에서 학습 대상 레코드 추출
            # - 접수종류명(ACC_TYPE_NAME), 계약전력(CONT_CAP), 총공사비(CONS_COST)
            # - 추후 계약종별/공급방식 관련 제약조건 추가 필요
            modeling_rows = \
                (df.acc_type_name == cfg.constraint.acc_type_name) & \
                (df.cont_cap       < cfg.constraint.max_cont_cap) & \
                (df.cons_cost      < cfg.constraint.max_total_cons_cost)
            df = df[modeling_rows].reset_index(drop=True)
            
            # 계약종별/공급방식 추가
            # (입력데이터와 동일한 방법으로 조정, 추후 조정 필요)
            df.loc[:, 'cont_type'] = '1'
            df.loc[:, 'sup_type'] = '1'
            
            # 사업소명을 간단히 영문4자로 변경
            # 추후 사업소 코드를 받기 때문에 이 부분은 별도로 필요없음
            office_names = df.office_name.unique().tolist()
            office_codes = []
            for oname in df.office_name:
                # 고유 사업소명의 순서에 따라 알파뱃 AAAA, BBBB..와 같이
                # 사업소 코드 부여
                ocode = f'{chr(ord("A")+office_names.index(oname))*4}'
                office_codes.append(ocode)
            df['office_cd'] = office_codes
            
            # 공사비 데이터셋 전처리 컬럼 추출
            self.cd_dict[id] = df[cfg.col.pp.cons.pp]
            
            # 전주/전선/인입선 데이터 중 공사비의 공사번호가 없는 레코드 제거
            # _df(설비df), df(공사비df)
            for id in cfg.type.pds.ids[1:]:
                _df = self._pd_dict[id]
                _df = _df[_df[cfg.col.join].isin(df[cfg.col.join])]
                self.cd_dict[id] = _df[eval(f'cfg.col.pp.{id}.pp')]
                
            # 크리닝 데이터 저장
            for id in cfg.type.pds.ids:
                save_data(self.cd_dict[id], f'data.cleaning.{id}')
                self._logs.mid(code=id, value=self.cd_dict[id].shape)
        except Exception as e:
            raise AiddsException(e)
            
            
            

