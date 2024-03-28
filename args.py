import argparse

def run_args():
    parser = argparse.ArgumentParser(
        description='Server-side Program of an Artificial Intelligence-based Distribution Design System',
        usage='Please use it as follows.\n' \
              '- cleaning: run -c(cleaning)'
              '- modeling: run [--modeling, -m] \n' \
              '- serving: run -s(--service) -d(--debug) [--port, -p] PORT-NO(default: 11001)', 
    )
    
    parser.add_argument(
        '--cleaning', '-c', action='store_true',
        help='The process of removeing unnecessary information and handling missing '\
             'values from the initial dataset to improve the quality of the data.'
    )
    parser.add_argument(
        '--modeling', '-m', action='store_true',
        help='Training artificial intelligence models. '\
             'If nothing is entered, the [--modeling] option will be applied automatically.'
    )
    parser.add_argument(
        '--serving', '-s', action='store_true',
        help='Starting a construction cont prediction service using AI models.'
    )
    parser.add_argument(
        '--debug', '-d', action='store_true',
        help='When running the web service, it is executed in debug mode to display '\
             'more error information.'
    )
    parser.add_argument(
        '--port', '-p', type=int, default=0,
        help='When specifying the port to be used for serving via the web, ' \
             'the default value is 11001'
    )
    args = parser.parse_args()
    return args

def serving_argvs():
    parser = argparse.ArgumentParser(
        description='Server-side Program of an Artificial Intelligence-based Distribution Design System'
    )
    parser.add_argument('--debug', '-d', action='store_true', help='')
    parser.add_argument('--port', '-p', type=int, default=11001, help='')

    args = parser.parse_args()
    return args