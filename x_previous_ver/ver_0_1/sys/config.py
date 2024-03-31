import os

# 디버그 모드
IS_DEBUG_MODE = False
# 로그 출력여부
IS_LOG_DISPLAY = True
IS_SERVICE_LOG_DISPLAY = True
# 웹 서비스 포트
PORT = 11001 

## 학습에 사용할 데이터 셋 종류
DATA_SETs = ['CONS', 'POLE', 'LINE', 'SL']

## 특정 컬럼의 값을 이용해 데이터 분리
## 여기서는 전주 갯 수를 이용해 데이터를 분리하고 있음
PC_TYPEs = ['ALL', '1', 'N1']       

## 모델링 데이터 셋
DATA_TYPEs = ['TRAIN_X', 'TEST_X', 'TRAIN_y', 'TEST_y']

## 데이터 기본 경로
BASE_PATH = os.path.join(os.path.expanduser('~'), 'projects', 'data', 'aidds')
## 시스템에서 사용할 파일명
FILE_NAMEs = {
    'PROVIDE': {
        'CONS': 'CONS_INFO.xlsx',
        'POLE': 'POLE_DATA.xlsx',
        'LINE': 'LINE_DATA.xlsx', 
        'SL': 'SL_DATA.xlsx',
    },
    'CLEANING': {
        'BATCH': {name: f'STEP01_MB_{name}.CSV' for name in DATA_SETs},
        'ONLINE': {name: f'STEP01_MO_{name}.CSV' for name in DATA_SETs},
    }, 
    'PP': {
        name: f'STEP0{idx+2}_PP_{name}.CSV' \
            for idx, name in enumerate(DATA_SETs)
    }, 
    'PP_LAST': 'STEP06_LAST_PREPROCESSING.CSV',
    'ONLINE': 'STEP06_ONLINE.CSV',  # 전처리된 시험용 최종 데이터
    'SCALING': {
        'X': {name: f'STEP07_X_{name}.CSV' for name in PC_TYPEs},
        'y': {name: f'STEP07_y_{name}.CSV' for name in PC_TYPEs},
        'TRAIN_X': {name: f'STEP08_TRAIN_X_{name}.CSV' for name in PC_TYPEs},
        'TEST_X': {name: f'STEP08_TEST_X_{name}.CSV' for name in PC_TYPEs},
        'TRAIN_y': {name: f'STEP09_TRAIN_y_{name}.CSV' for name in PC_TYPEs},
        'TEST_y': {name: f'STEP09_TEST_y_{name}.CSV' for name in PC_TYPEs},
    },
    'DUMP': {
        'OFFICE_LIST': 'MEM01_OFFICE_LIST.pkl',
        'POLE_ONE_HOT_COLS': 'MEM02_POLE_ONE_HOT_COLS.pkl',
        'LINE_ONE_HOT_COLS': 'MEM03_LINE_ONE_HOT_COLS.pkl',
        'SL_ONE_HOT_COLS': 'MEM04_SL_ONE_HOT_COLS.pkl',
        'LAST_PP_COLS': 'MEM05_LAST_PP_COLS.pkl',
        'MODELING_COLS': 'MEM05_MODELING_COLS.pkl',
        'SCALER': {name: f'MEM06_SCALER_{name}.pkl' for name in PC_TYPEs},
        # MEM07: 인공지능 모델 저장
        'MODELING_HISTORY': 'MEM08_MODELING_HISTORY.pkl',
    },
}

# 모델링에서 전처리를 위해 읽을 pickle파일 리스트
LOAD_PICKLEs = [
    'OFFICE_LIST', 'POLE_ONE_HOT_COLS', 'LINE_ONE_HOT_COLS',
    'SL_ONE_HOT_COLS', 'LAST_PP_COLS'
]

## 학습 데이터 제약조건
CONSTRAINTs = {
    'ACC_TYPE_NAME'         : '신설(상용/임시)',
    'MAX_CONT_CAP'          : 50,
    'CONS_TYPE_CD'          : 2,
    'MAX_TOTAL_CONS_COST'   : 30000000,
    'MIN_POLE_CNT'          : 1,
    'MAX_POLE_CNT'          : 10,
    'MIN_LINE_CNT'          : 1,
    'MAX_LINE_CNT'          : 11,
    'SL_CNT'                : 1,
} 

## 설비 연동 키 값
JOIN_COL = 'ACC_NO'
## 다양하게 사용될 컬럼들
COLs = {
    # 타겟 컬럼
    'TARGET': 'CONS_COST', 
    # 예측결과 리턴할 항목 리스트(현재 사용하지 않음)
    'RETURN': [JOIN_COL, 'CONS_COST'],
    # 전주 갯 수 확인 컬럼
    'PC': 'POLE_CNT',     # PC: POLE COUNT
    # 영문으로 변경할 컬럼들
    'RENAME': {
        '공사번호': JOIN_COL,               # Accept No
        '총공사비': 'CONS_COST',            # Total Construction Cost
        '최종변경일시': 'ACC_DATE',         # Last Modification Date and Time
        '사업소명': 'OFFICE_NAME',
        '계약전력': 'CONT_CAP',             # Contracted Capacity
        '공급방식': 'SUP_TYPE',
        '접수종류명': 'ACC_TYPE_NAME',      # Accept Type Name
        
        '전주형태코드': 'POLE_SHAPE_CD',
        '전주종류코드': 'POLE_TYPE_CD',
        '전주규격코드': 'POLE_SPEC_CD',
        'X좌표-Y좌표': 'COORDINATE',
        
        '결선방식코드': 'WIRING_SCHEME',
        '지지물간거리': 'SPAN',
        '전선종류코드1': 'LINE_TYPE_CD',
        '전선규격코드1': 'LINE_SPEC_CD',
        '전선조수1': 'LINE_PHASE_CD',
        '중성선종류코드': 'NEUTRAL_TYPE_CD',
        '중성선규격코드': 'NEUTRAL_SPEC_CD',
        
        '인입전선종류코드': 'SL_TYPE_CD',
        '고객공급선규격코드': 'SL_SPEC_CD',
        '인입선지지물간거리': 'SL_SPAN',
        '조수': 'SUPERVISOR',
    },

    # 전처리에 사용되는 컬럼들
    'PP': {
        'CONS': {
            'SOURCE': [
                JOIN_COL, 'CONS_COST',  
                'ACC_DATE', 'OFFICE_NAME', 
                'CONT_CAP', 'SUB_TYPE',
                'CONT_TYPE', 'ACC_TYPE_NAME' 
            ],
            'PRED': [
                JOIN_COL, 'CONS_COST',
                'PRED_NO', 'PRED_TYPE',  
                'ACC_DATE', 'OFFICE_CD',
                'CONT_CAP', 'SUB_TYPE'
            ],
            'PP_IN': [
                JOIN_COL, 'CONS_COST',  
                'ACC_DATE', 'OFFICE_CD', 
                'CONT_CAP', 'SUB_TYPE'
            ],
            'PP': [
                JOIN_COL, 'CONS_COST', 'OFFICE_NO', 'CONT_CAP', 'SUB_TYPE',
                'YEAR', 'MONTH', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'YEAR_MONTH',
            ],
        },
        'POLE': {
            'SOURCE': [
                JOIN_COL, 'POLE_SHAPE_CD', 'POLE_TYPE_CD', 'POLE_SPEC_CD',
                'COORDINATE'    
            ],
            'PRED': [
                JOIN_COL, 'POLE_SHAPE_CD', 'POLE_TYPE_CD', 'POLE_SPEC_CD',
                'GEO_X', 'GEO_Y',
            ],
            'PP_IN': [
                JOIN_COL, 'POLE_SHAPE_CD', 'POLE_TYPE_CD', 'POLE_SPEC_CD',
            ],
        },
        'LINE': {
            'SOURCE': [
                JOIN_COL, 
                'WIRING_SCHEME', 'LINE_TYPE_CD', 'LINE_SPEC_CD', 'LINE_PHASE_CD',
                'SPAN', 'NEUTRAL_TYPE_CD', 'NEUTRAL_SPEC_CD'
            ], 
        },
        'SL': {
            'SOURCE': [
                JOIN_COL, 'SL_TYPE_CD', 'SL_SPEC_CD', 'SL_SPAN', 'SUPERVISOR'
            ],
        }
    },

    # 모델학습에 사용할 중요 컬럼들
    'SPECIAL': [
        'CONT_CAP', 
        'YEAR_MONTH', 
        'EID_CODE_NUMBER', 'EID_NUMBER', 
        'OFFICE_NUMBER',
        'LINE_CNT', 
        'REAL_POLE_CNTS', 
        'SUPPORT_POLE_CNT', 
        'REAL_SL_CNTS', 'SL_SPAN_SUM',
        'POLE_SHAPE_O', 
        'POLE_TYPE_C', 'POLE_TYPE_H', 
        'POLE_SPEC_10.0', 'POLE_SPEC_12.0',
        'SPAN', 'LINE_LENGTH', 
        'WIRING_SCHEME_13', 'WIRING_SCHEME_43',
        'LINE_TYPE_AO', 'LINE_TYPE_C2', 'LINE_TYPE_OW',
        'LINE_SPEC_22.0', 'LINE_SPEC_35.0', 
        'LINE_PHASE_1', 
        'NEUTRAL_TYPE_AL', 'NEUTRAL_TYPE_WO', 'NEUTRAL_TYPE_ZZ', 
        'NEUTRAL_SPEC_0.0', 'NEUTRAL_SPEC_22.0', 'NEUTRAL_SPEC_32.0', 
        'POLE2_X', 'POLE2_Y',   
    ],
}

# 변경되지 않고 시스템에서 사용되는 값들

## AiddException에서 메시지 출력할 때 구분자로 줄바꿈 문자를 사용
EXCEPTION_DELIMITER = '\n'

## 폰트설정
WIN_FONT_PATH = 'c:/Windows/Fonts/malgun.ttf'
WIN_FONT_NAME = 'MalgunGothic'
UBUNTU_FONT_PATH = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
UBUNTU_FONT_NAME = 'NanumGothic'

# 학습에 사용할 모델 관련 데이터

# 학습에 관련된 사항들
from sklearn.linear_model import Lasso, Ridge, LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import ElasticNet
from xgboost import XGBRegressor
import lightgbm as lgbm

SEED = 1234
MODELs = {
    'ML': {
        'LIN': LinearRegression(),
        'LASSO': Lasso(max_iter=3000),
        'RIDGE': Ridge(),
        'KNR': KNeighborsRegressor(),
        'DTR': DecisionTreeRegressor(),
        'RFR': RandomForestRegressor(
            n_estimators=200, 
            n_jobs=-1, 
            random_state=SEED
        ),
        'GBR': GradientBoostingRegressor(),
        'EN': ElasticNet(
            alpha=0.1, 
            max_iter=1000,
            l1_ratio=0.5, 
            random_state=SEED
        ),
        'XGR': XGBRegressor(eta=0.01, n_estimators=100, n_jobs=-1),
        # 'LGBM': None, #추후 테스트 진행 후 추가 예정
    },
}
MODEL_KEYs = list(MODELs['ML'].keys())
FILE_NAMEs['DUMP']['MODELS'] = {
    pckey: {
        mname: f'MEM_07_MODEL_{pckey}_{mname}.pkl' \
            for mname in MODEL_KEYs+['BEST']
    } for pckey in PC_TYPEs
}