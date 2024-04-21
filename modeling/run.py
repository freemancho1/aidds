from aidds import app_init, modeling_logs, AppException
from aidds.modeling import Preprocessing, Scaling, Learning


def main():
    logs = modeling_logs(code='')    # Default 'modeling'
    try:
        app_init()
        pp = Preprocessing()
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