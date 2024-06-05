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


## Settings

# System
_sys = {
    # System conditions
    'cond': {
        # Debug Mode
        'debug_mode': True,
        # Determining whether to display logs
        'display_logs': {
            'modeling': True,
            'service': True
        }
    },
    # Web service
    'web': {
        'port': 11001,
    },
    # Matplotlib Font
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
        },
        'font_family': 'sans-serif',
    },
    # Etc.....
    'utils': {
        'trace': {
            'skip_lib': 'envs',
            'error_pattern': r'\n[A-Z].*?\n',
        },
        'data_io': {
            'index': 'index',
        }
    },
}

# Models
_models = {'seed': 1234}
_models['ml'] = {
    'lin': LinearRegression(),
    'lasso': Lasso(max_iter=3000),
    'ridge': Ridge(),
    'knr': KNeighborsRegressor(),
    'dtr': DecisionTreeRegressor(),
    'rfr': RandomForestRegressor(
        n_estimators=200, 
        n_jobs=-1, 
        random_state=_models['seed']
    ),
    'gbr': GradientBoostingRegressor(),
    'en': ElasticNet(
        alpha=0.1, 
        max_iter=1000,
        l1_ratio=0.5, 
        random_state=_models['seed']
    ),
    'xgr': XGBRegressor(eta=0.01, n_estimators=100, n_jobs=-1),
}
_models['key'] = list(_models['ml'].keys())

# Modeling settings
_modeling = {
    'test_size': 0.25,
    'cols': 'modeling_cols',
    'best': {
        'cnt': 5,
        'per': 0.85,  
    },
}

# Data type
_type = {
    # Provide DataSet
    'pds': ['cons', 'pole', 'line', 'sl'],
    # Training DataSet
    'tds': ['train_x', 'test_x', 'train_y', 'test_y']
}

# Constraints on modeling data
_constraints = {
    'acpt_knd_cd'               : '신설(상용/임시)',
    'max_cntr_pwr'              : 50,
    'max_total_cons_cost'       : 30000000,
    'min_pole_cnt'              : 0,
    'max_pole_cnt'              : 10,
    'min_line_cnt'              : 0,
    'max_line_cnt'              : 11,
    'sl_cnt'                    : 1,
} 

# Columns
_cols = {
    # Column to be used for joining
    'join'                      : 'acc_no',
    # Column to be used as the target for model training
    'target'                    : 'cons_cost'
}
_cols.update({
    # Columns to be translated into English
    'rename': {
        # cons
        '공사번호'              : _cols['join'],          # 'acc_no', Accept No
        '총공사비'              : _cols['target'],        # 'cons_cost', Total Construction Cost
        '최종변경일시'          : 'acc_date',             # Last Modification Date and Time
        '사업소코드'            : 'office_cd',
        '계약전력'              : 'cntr_pwr',             # Contracted Capacity
        '계약종별'              : 'cntr_type',
        '공급방식'              : 'sply_tpcd',
        '접수종류명'            : 'acpt_knd_cd',          # Accept Type Name
        # pole
        'CONS_NO'               : _cols['join'],
        'POLE_KND_CD'           : 'pole_knd_cd',
        'POLE_SPEC_CD'          : 'pole_spec_cd',
        'POLE_FORM_CD'          : 'pole_form_cd',
        # line
        '결선방식코드'          : 'wrng_mode_cd',
        '긍장'                  : 'span',
        '저압선종류코드'         : 'wire_knd_cd',
        '저압선규격코드'         : 'wire_spec_cd', 
        '조수코드'             : 'wire_lico', 
        '중성선종류코드'        : 'newi_knd_cd', 
        '중성선규격코드'        : 'newi_spec_cd',
        # sl
        '인입전선종류코드'      : 'sl_type_cd',
        '고객공급선규격코드'    : 'sl_spec_cd', 
        '인입선긍장'            : 'sl_span', 
        '인입선조수코드'        : 'sl_lico',
    },
    'cons': {
        'source': {
            'modeling': [
                _cols['join'], 
                _cols['target'],
                'office_name',
                'cntr_pwr',
                'cntr_type',
                'sply_tpcd',
                'acpt_knd_cd',
            ],
            'service': [
                _cols['join'],
                _cols['target'],  
                'pred_id',
                'pred_seq',
                'office_cd',
                'cntr_pwr',
                'cntr_type',
                'sply_tpcd',
            ],
        },
        'pp': [
            _cols['join'], 
            _cols['target'],
            'office_cd',
            'cntr_pwr',
            'cntr_type',
            'sply_tpcd',                    
        ],  
    }, 
    'pole': {
        'source': {
            'modeling': [
                _cols['join'],
                'pole_form_cd',
                'pole_knd_cd',
                'pole_spec_cd',
                'coordinate',
            ],
            'service': [
                _cols['join'],
                'pole_form_cd',
                'pole_knd_cd',
                'pole_spec_cd',
                'geo_x',
                'geo_y',
            ],
        },
        'pp': [
            _cols['join'],
            'pole_form_cd',
            'pole_knd_cd',
            'pole_spec_cd',
        ],
    },
    'line': {
        'pp': [
            _cols['join'],
            'wrng_mode_cd',
            'span',
            'wire_knd_cd',
            'wire_spec_cd',
            'wire_lico',
            'newi_knd_cd',
            'newi_spec_cd',
        ]
    },
    'sl': {
        'pp': [
            _cols['join'],
            'sl_type_cd',
            'sl_spec_cd',
            'sl_span',
            'sl_lico',
        ]
    }
})

_file = {
    'type': {
        'data'                  : 'data',
        'pickle'                : 'pickle',
        # Using: joblib
        'model'                 : 'model',
    },
    'ext': {
        'excel'                 : '.xlsx',
        'csv'                   : '.csv',
        'pickle'                : '.pkl',
        'model'                 : '.model',
    },
    'base_path': \
        os.path.join(
            os.path.expanduser('~'), 
            "projects", "data", "buy", "cost"
        ),
}
# Temporary variable for brevity
_xls = _file['ext']['excel']
_csv = _file['ext']['csv']
_pkl = _file['ext']['pickle']
_file.update({
    'name': {
        'data': {
            'provide': {
                pkey: f'{pkey}{_csv}' for pkey in _type['pds']
            },
            'cleaning': {
                pkey: f'data01_{pkey}_cleaning'+_csv \
                    for pkey in _type['pds']
            },
            'pp': {
                pkey: f'data02_{pkey}_pp'+_csv \
                    # 'zero' is a dataframe of data without pole for testing
                    # - Of these, 7 have wires, and 30 not wires.
                    for pkey in _type['pds'] + ['last', 'zero', 'best']
            },
            'split': {
                tkey: f'data03_split_{tkey}'+_csv \
                    for tkey in ['x','y'] + _type['tds']
            },
            'scaling': {
                tkey: f'data04_scaling_{tkey}'+_csv \
                    for tkey in ['x','y','best'] + _type['tds']   
            }
        },
        # Memory Data
        'pickle': {
            'office_codes': 'mem01_office_codes'+_pkl,
            'pole_one_hot_cols': 'mem02_pole_one_hot_cols'+_pkl,
            'line_one_hot_cols': 'mem03_line_one_hot_cols'+_pkl,
            'sl_one_hot_cols': 'mem04_sl_one_hot_cols'+_pkl,
            'last_pp_cols': 'mem05_last_pp_cols'+_pkl,
            'modeling_cols': 'mem06_modeling_cols'+_pkl,
            'scaler': 'mem07_scaler'+_pkl,
        },
        # Model Data: 
        # This model data is stored using joblib instead of pickle
        'model': {
            mkey: f'mem09_model_{mkey}'+_file['ext']['model'] \
                for mkey in _models['key'] + ['best']
        },
    }
})
    
# Convert dictionary to semi-class
# - to use attribute assignment, e.g., sys.cond.debug_mode = False
sys = DotMap(_sys)
models = DotMap(_models)
modeling = DotMap(_modeling)
type = DotMap(_type)
constraints = DotMap(_constraints)
cols = DotMap(_cols)
file = DotMap(_file)
