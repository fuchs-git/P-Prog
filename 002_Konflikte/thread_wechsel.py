from threading import Thread
from time import sleep

def anna():
    global anna_ist_dran
    while True:
        if anna_ist_dran:
            print('Anna geht schießen.')
            sleep(2)
            print('Anna passt auf Hund auf')
            anna_ist_dran = False

def paul():
    global anna_ist_dran
    while True:
        if not anna_ist_dran:
            print('Paul geht schießen.')
            sleep(2)
            print('Paul passt auf Hund auf')
            anna_ist_dran = True

anna_ist_dran = True

Thread(target=anna).start()
Thread(target=paul).start()