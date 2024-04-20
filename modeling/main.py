from aidds.sys.init import AppInit
from aidds.sys.utils.logs import ModelingLogs as Logs
from aidds.sys.utils.exception import AppException
from aidds.modeling.preprocessing import ModelingPreprocessing
from aidds.modeling.scaling import Scaling
from aidds.modeling.learning import Learning


def main():
    logs = Logs(code='')    # Default 'modeling'
    try:
        AppInit()
        pp = ModelingPreprocessing()
        sc = Scaling(pp_df=pp.ppdf)
        Learning(scaling_df_dict=sc.sdata)
    except KeyboardInterrupt as ke:
        raise AppException(ke)
    except Exception as e:
        raise AppException(e)
    finally:
        logs.stop()
        

if __name__ == '__main__':
    try:
        main()
    except AppException as ae:
        ae.print()
    except Exception as e:
        print(e)