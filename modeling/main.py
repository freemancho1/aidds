from aidds.sys.app_init import AiddsInit
from aidds.sys.utils.exception import AiddsException
from aidds.sys.utils.logs import ModelingLogs as Logs
from aidds.modeling.preprocess import Preprocessing
from aidds.modeling.scaler import Scaling
from aidds.modeling.learn import Learning


def main():
    try:
        logs = Logs(code='modeling')
        init = AiddsInit()
        init.run()
        pp = Preprocessing()
        sc = Scaling(is_best=True)
        Learning(scaling_data=sc.sdata)
    except KeyboardInterrupt as ke:
        raise AiddsException(ke)
    except Exception as e:
        raise AiddsException(e)
    finally:
        logs.stop()
        
if __name__ == '__main__':
    try:
        main()
    except AiddsException as ae:
        ae.print()
    except Exception as e:
        print(e)