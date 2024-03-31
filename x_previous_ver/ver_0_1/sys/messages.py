# 시스템 메시지
SYS = {
}

EXCEPIONs = {
    # 시스템 오류
    'EXCEPTION_ERR': 'An error occurred during the exception handling process.',
    'EXCEPTION_TEST': 'Exception test',
    
    # 모델링 오류
    'READ_DATA': 'Error reading data file',
    'SAVE_DATA': 'Error saving data file',
    'GET_PROVIDE_DATA': 'Error fetching provided data',
    'GET_CLEANING_DATA': 'Error fetching cleaning data',
    'CLEANING': 'Error cleaning provided data',
    'PP': 'Error preprocessing data',
    'PP_RUN': 'Error preprocessing data[_run()]',
    'PP_CONS': 'Error CONS data preprocessing',
    'PP_CONS_MD': 'Error CONS data preprocessing[Module]',
    'PP_CALCULATE': 'Error calculating dataset',
    'PP_CALCULATE_MD': 'Error calculating dataset[Module]',
    'PP_POLE': 'Error POLE data preprocessing',
    'PP_POLE_MD': 'Error POLE data preprocessing[Module]',
    'PP_LINE': 'Error LINE data preprocessing',
    'PP_LINE_MD': 'Error LINE data preprocessing[Module]',
    'PP_SL': 'Error SL data preprocessing',
    'PP_SL_MD': 'Error SL data preprocessing[Module]',
    'PP_CALCULATE_SUM': 'Error calculating facilities data',
    'SCALING_INIT': 'Error scaling init',
    'SCALING_RUN': 'Error scaling run',
    'SCALING_SPLIT': 'Error scaling split',
    
    # 서비스 메시지
    'STOP_SERVICE': 'Stop service!',
    'RUN_SERVICE': 'Error',
    # 서비스 오류
    'GET_SAMPLES': 'Extracting sample data.',
    'SERVICE_PP': 'Service preprocessing data.',
    'SERVICE_DTD': 'Service dictionary to dataframe.',
}

# Service 
ERRORs = {
    'ERR': 'error',
    '400': 'Invalid JSON',
}

LOGs = {
    'SYS': {
        'START': 'start.',
        'STOP': 'stop',
        'TOTAL': 'Total processing time',
        'NONE': '',
    },
    'MAIN': {
        'CLEANING': 'Data cleaning',
        'MODELING_MAIN': 'Data modeling',
        'GET_PROVIDE_DATA': 'Fetching provided data',
        'GET_CLEANING_DATA': 'Fetching cleaning data',
        'PP': 'Data preprocessing',
        'PP_CONS': 'CONS data preprocessing',
        'PP_CALCULATE': 'Calculating the number of facilities',
        'PP_POLE': 'POLE data preprocessing',
        'PP_LINE': 'LINE data preprocessing',
        'PP_SL': 'SL data preprocessing',
        'SCALING': 'Partitioning and Scaling of preprocessed data',
        'LEARNING': 'Model training',
        'SERVICE_PP': 'The preprocessing manager for the web service has started.',
        'SERVICE': 'Model serving',
    },
    'SUB': {
        'CLEANING': {
            'CONS': 'CONS data set',
            'POLE': 'POLE data set',
            'LINE': 'LINE data set',
            'SL': 'SL data set',
            'COL': 'Columns',
        },
        'GET_PROVIDE_DATA': {
            'CONS': 'CONS data set',
            'POLE': 'POLE data set',
            'LINE': 'LINE data set',
            'SL': 'SL data set',
        },
        'GET_CLEANING_DATA': {
            'CONS': 'Cleaned CONS',
            'POLE': 'Cleaned POLS',
            'LINE': 'Cleaned LINE',
            'SL': 'CLeaned SL',
        },
        'PP_CONS': {
            'SOURCE': 'CONS dataset size before preprocessing',
            'RESULT': 'CONS dataset size after preprocessing',
        }, 
        'PP_CALCULATE': {
            'CALCULATE': 'Dataset size after calculating and checking',
            # 'RESULT': 'Dataset size after check count',
        },
        'PP_POLE': {
            # 'SOURCE': 'POLE dataset size before preprocessing',
            'ONE_HOT': 'POLE dataset size after One-Hot Encoding',
            'RESULT': 'Modeling dataset size after POLE dataset One-Hot Encoding',
        },         
        'PP_LINE': {
            # 'SOURCE': 'LINE dataset size before preprocessing',
            'ONE_HOT': 'LINE dataset size after One-Hot Encoding',
            'RESULT': 'Modeling dataset size after LINE dataset One-Hot Encoding',
        }, 
        'PP_SL': {
            'ONE_HOT': 'SL dataset size after One-Hot Encoding',
            'RESULT': 'Modeling dataset size after SL dataset One-Hot Encoding',
        }, 
        'SCALING': {
            'SOURCE_X': '학습대상 속성 데이터 전체 크기',
            'PC_TYPE_X': '전주 수 타입',
            'PC_TYPE_TT': '전주 수 타입별 훈련/시험 데이터 크기'
        },
        'LEARNING': {
            'RESULT': '모델학습 결과',
        },
        'SERVICE_PP': {
            'MSG': '',  
        },
        'SERVICE': {
            'INPUT_ERR': 'JSON 이외의 데이터가 입력되었습니다.',
            'INPUT_OK': '입력 데이터',
        },
    },
}

SERVICE_LOGs = {
    'SERVICE': 'The construction cost prediction web service is ready. Please visit http://aidds.kdn.com:',
    'SERVICE_MID': {
        'DEBUG_MODE': 'This server is running in debug mode.',
        'PRODUCT_MODE': 'This server is running in product mode.', 
        'EXIT': 'When you press Ctrl+C, the service will be terminated.', 
    },
    'SERVICE_MGR': 'The service manager for the web service has started.',
    'ROUTE': 'The route manager for the web service has started.',
    'ROUTE_MID': {
        'ERROR': 'Error:',
    },
    'PREDICT': 'The predict manager for the web service has started.',
    'SAMPLE': 'The sample manager for the web service has started.',
}