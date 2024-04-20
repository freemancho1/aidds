from aidds.sys.init import AppInit
from aidds.sys.utils.exception import AppException
from aidds.cleaning.cleaning import Cleaning


def main():
    try:
        AppInit()
        Cleaning()
    except KeyboardInterrupt as ke:
        raise AppException(ke)
    except Exception as e:
        raise AppException(e)
    
    
if __name__ == '__main__':
    try:
        main()
    except AppException as ae:
        ae.print()
    except Exception as e:
        print(e)
