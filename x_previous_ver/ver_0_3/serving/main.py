from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from aidds_buy.args import serving_argvs
from aidds_buy.sys.app_init import AiddsInit
from aidds_buy.sys.utils.exception import AiddsException
from aidds_buy.sys.utils.logs import service_logs as logs

from aidds_buy.serving.restapi_server import app


def main(service_port=None, is_debug_mode=None):
    try:
        app.debug = is_debug_mode
        http_server = HTTPServer(WSGIContainer(app))
        http_server.listen(service_port)
        
        logs()
        logs(code='main', value=f'{service_port}/predict')
        logs(code='debug_mode' if is_debug_mode else 'product_mode')
        logs()
        logs(code='exit')
        logs()
        
        IOLoop.instance().start()
    except KeyboardInterrupt as _:
        logs()
        logs(code='shut_down')
        exit()
        # raise AiddsException(ke)
    except Exception as e:
        raise AiddsException(e)
        
        
if __name__ == '__main__':
    try:
        init = AiddsInit()
        init.run()
        argvs = serving_argvs()
        main(service_port=argvs.port, is_debug_mode=argvs.debug)
    except AiddsException as ae:
        ae.print()
    except Exception as e:
        print(e)