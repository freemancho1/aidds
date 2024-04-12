import os
from dotmap import DotMap
from datetime import datetime

from sklearn.linear_model import Lasso, Ridge, LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import ElasticNet
from xgboost import XGBRegressor
import lightgbm as lgbm

# 시스템 설정
_sys = {
    # 시스템 조건
    'case': {
        # 디버그 모드
        'debug_mode': False,
        # 로그 출력 여부
        'log_display': {
            'modeling': True,
            'service': True,
        }
    },
    # 웹 서비스 포트
    'web_service': {
        'port': 11001,
    },
    # 폰트 설정
    'font': {
        'win': {
            'osname': 'Windows',
            'path': 'c:/Windows/Fonts/malgun.ttf',
            'name': 'MalgunGothic',
        },
        'ubuntu': {
            'osname': 'Ubuntu',
            'path': '/usr/share/fonts/truetype/nanum/NanumGothic.ttf',
            'name': 'NanumGothic',
        }
    },
    # 기타
    ## config에서 사용하는 index 문자
    'indexes': 'ids',
    ## 데이터프레임 저장시 인덱스 추가에 사용
    'index': 'index',
    ## 피클 일기 쓰기
    'pickle': {
        'read': 'rb',
        'write': 'wb',
    }
}

# 학습 모델 정보
_model = {'seed': 1234}
_model['ml'] = {
    'lin': LinearRegression(),
    'lasso': Lasso(max_iter=3000),
    'ridge': Ridge(),
    'knr': KNeighborsRegressor(),
    'dtr': DecisionTreeRegressor(),
    'rfr': RandomForestRegressor(
        n_estimators=200, 
        n_jobs=-1, 
        random_state=_model['seed']
    ),
    'gbr': GradientBoostingRegressor(),
    'en': ElasticNet(
        alpha=0.1, 
        max_iter=1000,
        l1_ratio=0.5, 
        random_state=_model['seed']
    ),
    'xgr': XGBRegressor(eta=0.01, n_estimators=100, n_jobs=-1),
}
_model[_sys['indexes']] = list(_model['ml'].keys())

# 데이터 타입
_type = {
    'pds': {             # provide data set type
        'cons': 'cons',
        'pole': 'pole',
        'line': 'line',
        'sl': 'sl',
    },    
    'mds': {            # modeling data set type
        'train_x': 'train_x',
        'test_x': 'test_x',
        'train_y': 'train_y',
        'test_y': 'test_y',
    },
    'pc': {        # pole count type
        'all': 'all',
        '1': '1',
        'n1': 'n1',
    },
}
_type['pds'][_sys['indexes']] = list(_type['pds'].keys())
_type['mds'][_sys['indexes']] = list(_type['mds'].keys())
_type['pc'][_sys['indexes']] = list(_type['pc'].keys())


## 학습에 사용하는 컬럼 정보
## 학습 데이터 제약조건
_constraint = {
    'acc_type_name'             : '신설(상용/임시)',
    'max_cont_cap'              : 50,
    'cons_type_cd'              : 2,
    'max_total_cons_cost'       : 30000000,
    'min_pole_cnt'              : 1,
    'max_pole_cnt'              : 10,
    'min_line_cnt'              : 1,
    'max_line_cnt'              : 11,
    'sl_cnt'                    : 1,
} 
_col = {
    # 연동할 컬럼
    'join'                      : 'acc_no',
    # 학습 목표 컬럼
    'target'                    : 'cons_cost',
    # 전주 갯 수 확인 컬럼
    'pc'                        : 'pole_cnt',
    # 기본 컬럼들
    'base': {
        ## 공사비
        'acc_no'                : 'acc_no',         # Accept No
        'cons_cost'             : 'cons_cost',      # Total Construction Cost
        'acc_date'              : 'acc_date',       # Last Modification Date and Time
        'office_name'           : 'office_name',
        'office_cd'             : 'office_cd',
        'office_id'             : 'office_id',
        'cont_cap'              : 'cont_cap',       # Contracted Capacity
        'cont_type'             : 'cont_type',
        'sup_type'              : 'sup_type',
        'acc_type_name'         : 'acc_type_name',  # Accept Type Name
        'year'                  : 'year',
        'month'                 : 'month',
        'day'                   : 'day',
        'dayofweek'             : 'dayofweek',
        'dayofyear'             : 'dayofyear',
        'year_month'            : 'year_month',
        'pred_no'               : 'pred_no',
        'pred_type'             : 'pred_type',
        'pred_cost'             : 'pred_cost',
        ## 전주
        'pole_shape_cd'         : 'pole_shape_cd',
        'pole_type_cd'          : 'pole_type_cd',
        'pole_spec_cd'          : 'pole_spec_cd',
        'coordinate'            : 'coordinate',
        'geo_x'                 : 'geo_x',
        'geo_y'                 : 'geo_y',
        ## 전선
        'wiring_scheme'         : 'wiring_scheme',
        'span'                  : 'span',
        'line_type_cd'          : 'line_type_cd',
        'line_spec_cd'          : 'line_spec_cd',
        'line_phase_cd'         : 'line_phase_cd',
        'neutral_type_cd'       : 'neutral_type_cd',
        'neutral_spec_cd'       : 'neutral_spec_cd',
        ## 인입선
        'sl_type_cd'            : 'sl_type_cd',
        'sl_spec_cd'            : 'sl_spec_cd',
        'sl_span'               : 'sl_span',
        'sl_phase'              : 'sl_phase',       # 조수
    }
}
_col.update({
    # 영문으로 변경할 컬럼들
    'rename': {
        # 공사비
        '공사번호'              : _col['join'],                        # Accept No
        '총공사비'              : _col['base']['cons_cost'],           # Total Construction Cost
        '최종변경일시'          : _col['base']['acc_date'],            # Last Modification Date and Time
        '사업소명'              : _col['base']['office_name'],
        '계약전력'              : _col['base']['cont_cap'],            # Contracted Capacity
        '공급방식'              : _col['base']['sup_type'],
        '접수종류명'            : _col['base']['acc_type_name'],       # Accept Type Name
        # 전주
        '전주형태코드'          : _col['base']['pole_shape_cd'],
        '전주종류코드'          : _col['base']['pole_type_cd'],
        '전주규격코드'          : _col['base']['pole_spec_cd'],
        'X좌표_Y좌표'           : _col['base']['coordinate'],
        # 전선
        '결선방식코드'          : _col['base']['wiring_scheme'],
        '지지물간거리'          : _col['base']['span'],
        '전선종류코드1'         : _col['base']['line_type_cd'],
        '전선규격코드1'         : _col['base']['line_spec_cd'], 
        '전선조수1'             : _col['base']['line_phase_cd'], 
        '중성선종류코드'        : _col['base']['neutral_type_cd'], 
        '중성선규격코드'        : _col['base']['neutral_spec_cd'],
        # 인입선
        '인입전선종류코드'      : _col['base']['sl_type_cd'],
        '고객공급선규격코드'    : _col['base']['sl_spec_cd'], 
        '인입선지지물간거리'    : _col['base']['sl_span'], 
        '조수'                 : _col['base']['sl_phase'],
    },
    'pp': {
        'cons': {
            'source': {
                'modeling': [
                    _col['join'], 
                    _col['base']['cons_cost'],
                    _col['base']['acc_date'],   # 제거(공사일과 접수일은 다름)
                    _col['base']['office_name'],
                    _col['base']['cont_cap'],
                    _col['base']['sup_type'],
                    _col['base']['cont_type'],
                    _col['base']['acc_type_name'],
                ],
                'service': [
                    _col['join'],
                    _col['base']['cons_cost'],  # 서비스시는 공백값(시험시 테스트 용으로 사용)
                    _col['base']['pred_no'],
                    _col['base']['pred_type'],
                    _col['base']['acc_date'],   # 제거
                    _col['base']['office_cd'],
                    _col['base']['cont_cap'],
                    _col['base']['sup_type'],
                ],
            },
            'pp': [
                _col['join'], 
                _col['base']['cons_cost'],
                _col['base']['office_cd'],
                _col['base']['cont_cap'],
                _col['base']['sup_type'],                    
            ],
        },
        'pole': {
            'source': {
                'modeling': [
                    _col['join'],
                    _col['base']['pole_shape_cd'],
                    _col['base']['pole_type_cd'],
                    _col['base']['pole_spec_cd'],
                    _col['base']['coordinate'],
                ],
                'service': [
                    _col['join'],
                    _col['base']['pole_shape_cd'],
                    _col['base']['pole_type_cd'],
                    _col['base']['pole_spec_cd'],
                    _col['base']['geo_x'],
                    _col['base']['geo_y'],
                ],
            },
            'pp': [
                _col['join'],
                _col['base']['pole_shape_cd'],
                _col['base']['pole_type_cd'],
                _col['base']['pole_spec_cd'],
            ],
        },
        'line': {
            'pp': [
                _col['join'],
                _col['base']['wiring_scheme'],
                _col['base']['line_type_cd'],
                _col['base']['line_spec_cd'],
                _col['base']['line_phase_cd'],
                _col['base']['span'],
                _col['base']['neutral_type_cd'],
                _col['base']['neutral_spec_cd'],
            ]
        },
        'sl': {
            'pp': [
                _col['join'],
                _col['base']['sl_type_cd'],
                _col['base']['sl_spec_cd'],
                _col['base']['sl_span'],
                _col['base']['sl_phase'],
            ]
        }
    }
})

# 파일정보
_file = {
    'type': {
        'data': 'data',
        'pickle': 'pickle',
    },
    'ext': {
        'excel': '.xlsx',
        'csv': '.csv',
        'pickle': '.pkl',
    },
    'base_path': os.path.join(os.path.expanduser('~'), 'projects', 'data', 'aidds'),
    'name': {
        'data': {
            'provide': {
                id: f'{id}_data.xlsx' \
                    for id in _type['pds'][_sys['indexes']]
            },
            'cleaning': {
                id: f'step01_cleaning_{id}.csv' \
                    for id in _type['pds'][_sys['indexes']]
            },
            'pp': {
                id: f'step02_pp_{id}.csv' \
                    for id in _type['pds'][_sys['indexes']]+['last']
            },
            'split': {
                id1: {
                    id2: f'step03_split_{id1}_{id2}.csv' \
                        for id2 in _type['pc'][_sys['indexes']]
                } for id1 in ['x', 'y'] + _type['mds'][_sys['indexes']]
            },
            'scaling': {
                id1: {
                    id2: f'step04_scaling_{id1}_{id2}.csv' \
                        for id2 in _type['pc'][_sys['indexes']]
                } for id1 in _type['mds'][_sys['indexes']]
            },
        },
        'pickle': {
            'pp': {
                'office': {
                    'names': 'mem01_office_names.pkl',
                    'codes': 'mem01_office_codes.pkl',
                },
                'one_hot_cols': {
                    'pole': 'mem02_one_hot_cols_pole.pkl',
                    'line': 'mem03_one_hot_cols_line.pkl',
                    'sl': 'mem04_one_hot_cols_sl.pkl',
                },
                'last_cols': 'mem05_pp_last_cols.pkl',
            },
            'modeling_cols': 'mem06_modeling_cols.pkl',
            'scaler': {
                id: f'mem07_scaler_{id}.pkl' \
                    for id in _type['pc'][_sys['indexes']]
            },
            'models': {
                id1: {
                    id2: f'mem08_model_{id1}_{id2}.pkl' \
                        for id2 in _model[_sys['indexes']] + ['best']
                } for id1 in _type['pc'][_sys['indexes']]
            },
            'modeling_history': 
                f'mem09_mh_{datetime.now().strftime("%Y%m%d%H%M%S")}.pkl'
        }
    }
}

sys = DotMap(_sys)
model = DotMap(_model)
type = DotMap(_type)
constraint = DotMap(_constraint)
col = DotMap(_col)
file = DotMap(_file)
