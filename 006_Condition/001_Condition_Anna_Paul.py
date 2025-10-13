'''
Wechselseitiger Ausschluss - mit einer Condition
'''

from threading import Thread, Condition
from time import sleep
from random import randint


def job(name: int):
    global schiessbahn_frei
    while True:
        sleep(randint(1, 10) / 10)
        print(f'{name} will schießen 🔥🧨🔥')
        with condition:
            while not schiessbahn_frei:
                print(f'{name} muss noch warten, der Hund darf nicht alleine sein 🐕‍🦺 ')
                condition.wait()
            schiessbahn_frei = False

        print(f'{name} geht schießen 🔫')
        sleep(randint(1, 10) / 10)

        with condition:
            print(f'{name} passt auf den Hund auf ')
            schiessbahn_frei = True
            condition.notify()


condition = Condition()
schiessbahn_frei = True
Thread(target=job, args=('Anna',)).start()
Thread(target=job, args=('Paul',)).start()
