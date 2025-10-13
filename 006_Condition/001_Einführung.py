'''
Wechselseitiger Ausschluss - mit einer Condition
'''

from threading import Thread, Condition
from time import sleep
from random import randint


def job(nummer: int):
    global schiessbahn_frei
    while True:
        sleep(randint(1, 10) / 10)
        with condition:
            while not ausgabe_frei:
                condition.wait()
            ausgabe_frei = False

        print(f'Job Nummer {nummer} betritt den kritischen Bereich')
        sleep(randint(1, 10) / 10)
        print(f'Job Nummer {nummer} verlässt den kritischen Bereich')

        with condition:
            ausgabe_frei = True
            condition.notify()


condition = Condition()
schiessbahn_frei = True
Thread(target=job, args=(2,)).start()
Thread(target=job, args=(1,)).start()
