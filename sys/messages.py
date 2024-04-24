from dotmap import DotMap

_log = {
    'sys': {
        'start': 'start.',
        'stop': 'end.',
        'total': ', Total processing time:',
    },
    'modeling': {
        'main': 'Data modeling',
        'cleaning': {
            'main': 'Cleaning provided data',
            'cons': 'CONS dataset cleaning',
            'pole': 'POLE dataset cleaning', 
            'line': 'LINE dataset cleaning',
            'sl': 'SL dataset cleaning', 
        },
        'get_provide_data': {
            'main': 'Fetching provided data',
            'cons': 'Get CONS dataset',
            'pole': 'Get POLE dataset',
            'line': 'Get LINE dataset',
            'sl': 'Get SL dataset',
        },
        'get_cleaning_data': {
            'main': 'Fetching cleaning data',  
            'cons': 'Get cleaning CONS dataset',
            'pole': 'Get cleaning POLE dataset',
            'line': 'Get cleaning LINE dataset',
            'sl': 'Get cleaning SL dataset',
        },
        'preprocessing': {
            'main': 'Data preprocessing for modeling part',
            'cons': {
                'main': 'CONS dataset preprocessing',
                'source': 'CONS dataset size before preprocessing',
                'result': 'CONS dataset size after preprocessing',
                'calculate': 'Preprocessing Dataset size after calculating and checking',
            },
            'pole': {
                'main': 'POLE dataset preprocessing',
                'one_hot': 'POLE dataset size after One-Hot Encoding',
                'result': 'Modeling dataset size merged with One-Hot POLE dataset',
            },
            'line': {
                'main': 'LINE dataset preprocessing',
                'one_hot': 'LINE dataset size after One-Hot Encoding',
                'result': 'Modeling dataset size merged with One-Hot LINE dataset',
            },
            'sl': {
                'main': 'SL dataset preprocessing',
                'one_hot': 'SL dataset size after One-Hot Encoding',
                'result': 'Modeling dataset size merged with One-Hot SL dataset',
            },
        },
        'scaling': {
            'main': 'Preprocessing data scaling',
            'source_x': 'Total size of attribute data for learning',
            'split': 'Data size of training/testing data',
        },
        'learning': {
            'main': 'Learning',
            'size': 'Modeling data size',
            'best': 'Change best model',
            'result': 'Model training results',
        },
    },
    'service': {
        'main': 'The construction cost prediction web service is ready. Please visit http://aidds.kdn.com:',
        'debug_mode': 'This server is running in debug mode.',
        'product_mode': 'This server is running in product mode.', 
        'exit': 'When you press Ctrl+C, the service will be terminated.', 
        'samples': {
            'main': 'The sample manager for the web service has started.',
            'samples': 'Accept numbers of sample data:',
        },
        'predict': {
            'main': 'The predic manager for the web service has started.',
            'json_size': 'Prediction request data size:',
            'result': 'Predict result:',
        },
        'manager': 'The service manager for the web service has started.',
        'exception': 'The system has terminated unexpectedly for an unknown reason.',
        'shut_down': 'The system has been shut down at the request of the administrator.'
    },
}

_exception = {
    'sys': {
        'error_endswith': '***',
        'head_message': ' ::: [AiddsError] ',
        'exception': 'The system has terminated unexpectedly for an unknown reason.',
        'unknown_file_ext': 'Unknown file extension error, the extension is',
    },
    'hc_msg': {
        'ok': 'Service Ok',
        'cr': 'Service Ok, Data has been created',
        'nc': 'Service Ok, But no data returned',
        'e400': 'The browser (or proxy) sent a request that this server could not understand.',
        'e401': 'The server could not verify that you are authorized to access the URL requested.',
        'e403': 'You don\'t have the permission to access the requested resource. It is either read-protected or not readable by the server.',
        'e404': 'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.',
        'e405': 'No access permission for the requested method',
        'e500': 'The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.',
        # 'br': 'Service requested incorrectly',
        # 'ua': 'Authentication request for service execution failed',
        # 'fb': 'No access permission for the service or data',
        # 'nf': 'The requested service could not be found',
        # 'mna': 'No access permission for the requested method',
        # 'ise': 'Internal server error'        
    },
    'web': {
        'bad_json': 'An error in the request JSON data',
    }
}

log = DotMap(_log)
exception = DotMap(_exception)