from aidds.sys.app_init import AiddsInit
from aidds.sys.utils.logs import ModelingLogs as Logs
from aidds.sys.utils.exception import AiddsException
from aidds.modeling.preprocessing import Preprocessing
from aidds.modeling.scaler import Scaling
from aidds.modeling.learning import Learning

import aidds.sys.messages as msg


def main():
    try:
        logs = Logs('MODELING_MAIN')
        AiddsInit()
        pp = Preprocessing()
        sc = Scaling(preprocessing_data=pp.pdf)
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