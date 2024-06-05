from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from aidds_buy.sys.app_init import AiddsInit
from aidds_buy.sys.utils.exception import AiddsException
from aidds_buy.sys.utils.logs import service_logs as logs

import aidds_buy.sys.messages as msg
from aidds_buy.args import serving_argvs

from aidds_buy.serving.rest_server import app


def main(service_port=None, is_debug_mode=None):
    try:
        app.debug = is_debug_mode
        http_server = HTTPServer(WSGIContainer(app))
        http_server.listen(service_port, 'dev.aidds.kdn.com')
        
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
        raise AiddsException(f'{msg.EXCEPIONs["EXCEPTION"]}\n{str(e)}')
        
if __name__ == '__main__':
    try:
        AiddsInit()
        args = serving_argvs()
        main(service_port=args.port, is_debug_mode=args.debug)
    except AiddsException as ae:
        ae.print()   