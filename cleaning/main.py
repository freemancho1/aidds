from aidds.sys.app_init import AiddsInit
from aidds.sys.utils.exception import AiddsException
from aidds.cleaning.cleaning import Cleaning


def main():
    try:
        AiddsInit()
        Cleaning()    
    except KeyboardInterrupt as ke:
        raise AiddsException(ke)
    except AiddsException as ae:
        ae.print()
    # except Exception as e:
    #     print('The system has terminated unexpectedly for an unknown reason.')
        
if __name__ == '__main__':
    main()