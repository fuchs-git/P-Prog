from threading import Thread
from time import sleep

def anna():
    global anna_will_schiessen, paul_will_schiessen, anna_war_grad_dran
    while True:
        anna_will_schiessen = True
        while paul_will_schiessen:
            if anna_war_grad_dran:
                anna_will_schiessen = False
                while anna_war_grad_dran:
                    pass
                anna_will_schiessen = True

        print('Anna geht schießen.')
        sleep(2)

        anna_war_grad_dran = True
        anna_will_schiessen = False

        print('Anna passt auf Hund auf')

def paul():
    global anna_will_schiessen, paul_will_schiessen, anna_war_grad_dran
    while True:
        paul_will_schiessen = True
        while anna_will_schiessen:
            if not anna_war_grad_dran:
                paul_will_schiessen = False
                while not anna_war_grad_dran:
                    pass
                paul_will_schiessen = True

        print('Paul geht schießen.')
        sleep(2)

        anna_war_grad_dran = False
        paul_will_schiessen = False

        print('Paul passt auf Hund auf')


# Variablen zur Synchronisation
anna_will_schiessen = False
paul_will_schiessen = False
anna_war_grad_dran = False


Thread(target=anna).start()
Thread(target=paul).start()