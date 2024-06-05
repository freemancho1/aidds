import aidds_buy.sys.message as msg
from aidds_buy.sys.app_init import AiddsInit
from aidds_buy.sys.utils.exception import AiddsException
from aidds_buy.cleaning.cleaning import Cleaning


def main():
    try:
        init = AiddsInit()
        init.run()
        Cleaning()
    except KeyboardInterrupt as ke:
        raise AiddsException(ke)
    except Exception as e:
        raise AiddsException(e)
    
if __name__ == '__main__':
    try:
        main()
    except AiddsException as ae:
        ae.print()
    except Exception as e:
        print(e)