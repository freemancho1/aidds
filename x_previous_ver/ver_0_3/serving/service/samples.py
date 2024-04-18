import json
import random

import aidds.sys.config as cfg
from aidds.sys.utils.exception import AiddsException
from aidds.sys.utils.logs import service_logs as logs
from aidds.sys.utils.data_io import read_data, get_cleaning_data


class Samples:
    """ 크리닝된 데이터에서 웹 서비스 테스트에 사용할 sample 데이터 생성 클래스
    
    Attributes:
        _source_df (pd.DataFrame): 전처리 완료된 BEST 데이터셋 데이터프레임
        _acc_nos           (list): 데이터프레임에서 acc_no들만 뽑은 리스트
        _cd_dict           (dict): 크리닝된 데이터셋들의 딕셔너리
    """
    def __init__(self):
        try:
            self._source_df = read_data(
                file_code='data.pp.best', dtype={cfg.col.join: str})
            self._acc_nos = self._source_df[cfg.col.join].tolist()
            self._cd_dict = get_cleaning_data()
            logs(code='samples.main')
        except Exception as e:
            raise AiddsException(e)
        
    def get(self, recommend_count=3) -> json:
        """ 서비스 테스트용 셈플 데이터(JSON) 1개를 리턴함
            - 셈플 데이터는 추천(제안) 경로 데이터 갯 수로 구성된 하나의 JSON임

        Args:
            recommend_count (int, optional): 생성할 추천(제안) 데이터 수. Defaults to 3.

        Returns:
            json: 서비스 테스트용 셈플 데이터
        """
        try:
            # 셈플에 사용할 acc_no를 recommend_count 만큼 추출
            sample_acc_nos = random.sample(self._acc_nos, k=recommend_count)
            logs(value=f'sample_acc_nos={sample_acc_nos}')
            
            # 셈플 데이터 생성
            sample_dict = {}
            for acc_no in sample_acc_nos:
                recommend_dict = {}
                for pds_id in cfg.type.pds.ids:
                    df = self._cd_dict[pds_id]
                    df = df[df[cfg.col.join] == acc_no]
                    recommend_dict[pds_id] = df
                # 셈플 데이터에 추천 경로 추가
                # - 단, 여기서는 접수번호(acc_no)가 각각 독립적임(각각 다름)
                sample_dict[acc_no] = recommend_dict
                
            # 추출된 셈플 데이터를 JSON으로 변환
            # 접수번호를 최초 접수번호로 통일하고 추천번호를 달리 부여함
            sample_json = self._sample_to_json(sample=sample_dict)
            return sample_json
        except Exception as e:
            raise AiddsException(e)
        
    def _sample_to_json(self, sample=None) -> json:
        """ 추출된 셈플 데이터를 JSON으로 변환하는 함수

        Args:
            sample (_type_, required): recommend_count 만큼 구성된
                하나의 셈플 데이터 딕셔너리. Defaults to None.

        Returns:
            json: 셈플 데이터 딕셔너리을 크리닝해 JSON으로 변환한 데이터
        """
        try:
            cleaning_dict = {}      # JSON으로 변경할 크리닝된 셈플 데이터
            sample_dict = sample
            acc_no = None           # 해당 셈플을 대표할 접수번호(가장 먼저오는 접수번호)
            pred_no = 1             # 추천 경로번호(1부터 시작함)
            
            for idx, row in sample_dict.items():
                pred_id = f'pred_{pred_no}'
                # 추천경로 데이터 저장 공간 확보
                cleaning_dict[pred_id] = {}
                # 셈플 데이터의 접수번호 지정(없으면 최초 번호)
                if acc_no is None:
                    acc_no = idx    # 딕셔너리에서는 idx에 키값이 옴
                    
                # 데이터 크리닝
                ## 각 추천번호별 공사번호(통일), pred_no, pred_type 추가
                ## - 최초에는 아래와 같음
                ##             acc_no  cons_cost office_cd  cont_cap  sup_type
                ## 3219  476920214453    2969453      CCCC         3         1
                cons_dict = row[cfg.type.pds.cons].to_dict(orient='records')[0]
                ## 공사번호 변경, 컬럼 추가
                cons_dict.update({
                    cfg.col.join: acc_no, 
                    'pred_no': pred_id, 'pred_type': pred_id
                })
                cleaning_dict[pred_id][cfg.type.pds.cons] = cons_dict
                
                # 각 추천번호별 설비정보 추가
                cleaning_dict[pred_id].update({
                    cfg.type.pds.pole: {},
                    cfg.type.pds.line: {},
                    cfg.type.pds.sl: {}
                })
                for pds_id in cfg.type.pds.ids[1:]:
                    df = row[pds_id].copy()
                    # 각 추천번호별 설비 세부정보 추출
                    fc_dict = {}
                    fc_seq = 1  # 설비 세부정보 일련번호는 1번부터 시작
                    for _, fc_row in df.iterrows():
                        _dict = fc_row.to_dict()
                        # 각 설비 세부정보의 접수번호를 최초 접수번호로 변경
                        _dict[cfg.col.join] = acc_no
                        fc_dict[f'{pds_id}_{fc_seq}'] = _dict
                        fc_seq += 1
                    cleaning_dict[pred_id][pds_id] = fc_dict
                pred_no += 1
            # 크리닝된 딕셔너리 JSON으로 변환
            sample_json = json.dumps(cleaning_dict, ensure_ascii=False)
            return sample_json
        except Exception as e:
            raise AiddsException(e)
        
        
