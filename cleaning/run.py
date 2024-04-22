from aidds.sys import app_init
from aidds.sys.utils import app_exception
from aidds.cleaning import cleaning


def main():
    try:
        app_init()
        cleaning()
    except KeyboardInterrupt as ke:
        raise app_exception(ke)
    except Exception as e:
        raise app_exception(e)
    
    
if __name__ == '__main__':
    try:
        main()
    except app_exception as ae:
        ae.print()
    except Exception as e:
        print(e)
