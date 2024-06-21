from aidds_buy.sys import app_init
from aidds_buy.sys.utils import modeling_logs as logs
from aidds_buy.sys.utils import app_exception
from aidds_buy.modeling import preprocessing
from aidds_buy.modeling import scaling
from aidds_buy.modeling import learning


def main():
    _logs = logs(code='')    # Default 'modeling'
    try:
        app_init()
        pp = preprocessing()
        sc = scaling(pp_df=pp.ppdf)
        learning(scaling_df_dict=sc.sdata)
        # learning()
    except KeyboardInterrupt as ke:
        raise app_exception(ke)
    except Exception as e:
        raise app_exception(e)
    finally:
        _logs.stop()
        

if __name__ == '__main__':
    try:
        main()
    except app_exception as ae:
        ae.print()
    except Exception as e:
        print(e)