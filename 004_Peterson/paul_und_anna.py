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


def job(thread_number):
    global counter
    for i in range(100):
        sleep(randint(1, 10) / 10)

        # kritischer bereich
        enter_region(thread_number)
        c = counter
        sleep(randint(1, 10) / 10)
        counter = c + 1
        leave_region(thread_number)


counter = 0
turn = 0
interested = [False, False]
Thread(target=job, args=(0,)).start()
Thread(target=job, args=(1,)).start()

while True:
    sleep(1)
    print(counter)
