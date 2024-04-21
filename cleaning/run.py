from aidds import app_init, AppException
from aidds.cleaning import cleaning


def main():
    try:
        app_init()
        cleaning()
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
