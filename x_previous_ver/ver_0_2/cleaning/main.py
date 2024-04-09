from aidds.sys.app_init import AiddsInit
from aidds.sys.utils.exception import AiddsException
from aidds.cleaning.cleaning import Cleaning

import aidds.sys.messages as msg


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