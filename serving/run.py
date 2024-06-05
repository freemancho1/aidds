from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from aidds_buy.sys import app_init
from aidds_buy.sys.utils import app_exception
from aidds_buy.sys.utils import service_logs as logs
from aidds_buy.args import serving_argvs

from aidds_buy.serving import app


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
        print()
        logs(code='shut_down')
        exit()
        # raise app_exception(ke)
    except Exception as e:
        raise app_exception(e)
        
        
if __name__ == '__main__':
    try:
        app_init()
        argvs = serving_argvs()
        main(service_port=argvs.port, is_debug_mode=argvs.debug)
    except app_exception as ae:
        ae.print()
    except Exception as e:
        print(e)