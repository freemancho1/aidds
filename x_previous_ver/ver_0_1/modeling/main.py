from aidds.sys.utils import AiddsInit as init
from aidds.sys.utils import Logs, AiddsException
from modeling.preprocess import Preprocessing


def main():
    logs = Logs('MODELING_MAIN')
    
    try:
        pp = Preprocessing()
    except AiddsException as ae:
        print(f'Error:\n{ae}')
    finally:
        logs.stop()
        
if __name__ == '__main__':
    init()
    main()