from aidds_buy.sys.app_init import AiddsInit
from aidds_buy.sys.utils.exception import AiddsException
from aidds_buy.cleaning.cleaning import Cleaning

import aidds_buy.sys.messages as msg


def main():
    try:
        AiddsInit()
        Cleaning()    
    except (KeyboardInterrupt, AiddsException) as ae:
        raise AiddsException(ae)
    except Exception as e:
        raise AiddsException(msg.EXCEPIONs['EXCEPTION'])
        
if __name__ == '__main__':
    try:
        main()
    except AiddsException as ae:
        ae.print()