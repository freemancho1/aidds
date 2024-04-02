from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from aidds.sys.app_init import AiddsInit
from aidds.sys.utils.exception import AiddsException
from aidds.sys.utils.logs import service_logs as logs

import aidds.sys.messages as msg
from aidds.args import serving_argvs

from aidds.serving.rest_server import app


def main(service_port=None, is_debug_mode=None):
    try:
        app.debug = is_debug_mode
        http_server = HTTPServer(WSGIContainer(app))
        http_server.listen(service_port)
        
        logs()
        logs(mcode='SERVICE', value=f'{service_port}/predict')
        mode_key = 'DEBUG_MODE' if is_debug_mode else 'PRODUCT_MODE'
        logs(mcode=mode_key)
        logs(mcode='EXIT')
        logs()
        
        IOLoop.instance().start()
    except (KeyboardInterrupt, AiddsException) as ae:
        raise AiddsException(ae)
    except Exception as e:
        raise AiddsException(msg.EXCEPIONs['EXCEPTION'])
        
if __name__ == '__main__':
    try:
        AiddsInit()
        args = serving_argvs()
        main(service_port=args.port, is_debug_mode=args.debug)
    except AiddsException as ae:
        ae.print()   