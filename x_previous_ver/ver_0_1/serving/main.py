from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from aidds.sys.utils import AiddsInit as aidds_init
from aidds.sys.utils import AiddsException
from aidds.sys.utils import ServiceLogs as Logs
from aidds.args import serving_argvs
import aidds.sys.messages as msg
from aidds.serving.rest_server import app

def main(s_port=None, is_debug=False):
    try:
        app.debug = is_debug
        http_server = HTTPServer(WSGIContainer(app))
        http_server.listen(s_port)
        
        print('\n')
        logs = Logs(code='SERVICE', value=f'{s_port}/predict')
        mode_key = 'DEBUG_MODE' if is_debug else 'PRODUCT_MODE'
        logs.mid(code=mode_key)
        logs.mid(code='EXIT')
        print('\n')
        IOLoop.instance().start()
    except KeyboardInterrupt:
        raise AiddsException('STOP_SERVICE')
    except Exception as e:
        raise AiddsException('RUN_SERVICE', se_msg=e) 
    
if __name__ == '__main__':
    try:
        aidds_init()
        args = serving_argvs()
        main(s_port=args.port, is_debug=args.debug)
    except Exception as e:
        print(f'[SERVICE] {e}')