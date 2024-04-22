from aidds import app_init, modeling_logs, app_exception
from aidds.modeling import Preprocessing, Scaling, Learning


def main():
    logs = modeling_logs(code='')    # Default 'modeling'
    try:
        app_init()
        pp = Preprocessing()
        sc = Scaling(pp_df=pp.ppdf)
        Learning(scaling_df_dict=sc.sdata)
    except KeyboardInterrupt as ke:
        raise app_exception(ke)
    except Exception as e:
        raise app_exception(e)
    finally:
        logs.stop()
        

if __name__ == '__main__':
    try:
        main()
    except app_exception as ae:
        ae.print()
    except Exception as e:
        print(e)