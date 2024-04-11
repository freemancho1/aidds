from dotmap import DotMap


_log = {
    'sys': {
        'start': 'start.',
        'stop': 'end.',
        'total': ', Total processing time:',
    },
    'modeling': {
        'get_provide_data': {
            'main': 'Fetching provided data',
            'cons': 'Get CONS dataset',
            'pole': 'Get POLE dataset',
            'line': 'Get LINE dataset',
            'sl': 'Get SL dataset',
        },
        'cleaning': {
            'main': 'Cleaning provided data',
            'cons': 'CONS dataset cleaning',
            'pole': 'POLE dataset cleaning',
            'line': 'LINE dataset cleaning',
            'sl': 'SL dataset cleaning',
        },
        'get_cleaning_data': {
            'main': 'Fetching cleaning data',  
            'cons': 'Get cleaning CONS dataset',
            'pole': 'Get cleaning POLE dataset',
            'line': 'Get cleaning LINE dataset',
            'sl': 'Get cleaning SL dataset',
        },
        'pp': {
            'main': 'Data preprocessing',
            'cons': {
                'main': 'CONS dataset preprocessing',
                'source': 'CONS dataset size before preprocessing',
                'result': 'CONS dataset size after preprocessing',
                'calculate': 'Preprocessing Dataset size after calculating and checking',
            },
        },

    }
}

_exception = {
    'sys': {
        'error_endswith': '***',
        'head_message': '\n::: [AiddsError] ',
        'exception': 'The system has terminated unexpectedly for an unknown reason.',
        'unknown_file_ext': 'Unknown file extension error, the extension is',
    },
}

log = DotMap(_log)
exception = DotMap(_exception)