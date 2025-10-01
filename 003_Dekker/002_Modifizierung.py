from threading import Thread
from time import sleep


def enter(x):
    global anna_will_schiessen, paul_will_schiessen, anna_war_grad_dran
    if x == 'a':
        anna_will_schiessen = True
        while paul_will_schiessen:
            if anna_war_grad_dran:
                anna_will_schiessen = False
                while anna_war_grad_dran:
                    pass
                anna_will_schiessen = True

        sleep(2)
    else:
        paul_will_schiessen = True
        while anna_will_schiessen:
            if not anna_war_grad_dran:
                paul_will_schiessen = False
                while not anna_war_grad_dran:
                    pass
                paul_will_schiessen = True

        sleep(2)


def leave(x):
    global anna_will_schiessen, paul_will_schiessen, anna_war_grad_dran
    if x == 'a':
        anna_war_grad_dran = True
        anna_will_schiessen = False
    else:
        anna_war_grad_dran = False
        paul_will_schiessen = False


def anna():
    global anna_will_schiessen, paul_will_schiessen, anna_war_grad_dran
    while True:
        enter('a')
        print('Anna geht schießen.')
        leave('a')
        print('Anna passt auf Hund auf')


def paul():
    global anna_will_schiessen, paul_will_schiessen, anna_war_grad_dran
    while True:
        enter('p')
        print('Paul geht schießen.')
        leave('p')
        print('Paul passt auf Hund auf')


# Variablen zur Synchronisation
anna_will_schiessen = False
paul_will_schiessen = False
anna_war_grad_dran = False

Thread(target=anna).start()
Thread(target=paul).start()
