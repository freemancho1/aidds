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
            'columns': 'Columns'
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