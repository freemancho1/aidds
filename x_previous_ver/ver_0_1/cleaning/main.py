from aidds.sys.utils import AiddsInit as init
from aidds.sys.utils import AiddsException
from aidds.cleaning.cleaning import Cleaning


def main():
    try:
        init()
        Cleaning()
    except AiddsException as ae:
        print(f'Error:\n{ae}')
        

if __name__ == '__main__':
    main()