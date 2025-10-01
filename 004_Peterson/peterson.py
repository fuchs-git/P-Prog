from random import randint
from threading import Thread
from time import sleep


def enter_region(thread_number):
    global interested, turn
    other = 1 - thread_number
    interested[thread_number] = True
    turn = other

    while interested[other] and turn == other:
        pass


def leave_region(thread_number):
    global interested
    interested[thread_number] = False


def anna():
    while True:
        enter_region(0)
        print('Anna geht schießen.')
        sleep(2)
        print('Anna ist fertig.')
        leave_region(0)
        print('Anna passt auf Hund auf')

def paul():
    while True:
        enter_region(0)
        print('Paul geht schießen.')
        sleep(2)
        print('Paul ist fertig.')
        leave_region(1)
        print('Paul passt auf Hund auf')



turn = 0
interested = [False, False]
Thread(target=anna).start()
Thread(target=paul).start()

