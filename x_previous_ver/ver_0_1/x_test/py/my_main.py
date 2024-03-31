from aidds.x_previous_ver.ver_0_1.x_test.py.my_exception import MyException, MyLog

def free_fn():
    try:
        log = MyLog()
        log.mid()
        a = 10/0
    except Exception as e:
        raise MyException(e)
    

class Freeman:
    def free_main(self):
        try:
            log = MyLog()
            log.mid()
            free_fn()
        except MyException as me:
            raise MyException(me)
        except Exception as e:
            raise MyException(e)
    
    
if __name__ == '__main__':
    try:
        f = Freeman()
        f.free_main()
    except MyException as me:
        me.print()
    except Exception as e:
        print(e)