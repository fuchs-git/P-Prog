'''
Wechselseitiger Ausschluss - Mutex
der Begriff wechselseitiger Ausschluss bzw. Mutex (Abk. für englisch mutual exclusion) bezeichnet eine Gruppe
von Verfahren, mit denen das Problem des kritischen Abschnitts gelöst wird.
Wir nutzen das Threading Modul 'Lock'
'''

from threading import Thread, Lock
from time import sleep
from random import randint


def anna():
    while True:
        sleep(randint(1, 10) / 10)
        print('Anna will schießen')

        lock.acquire()
        print('Anna geht schießen')
        sleep(randint(1, 10) / 10)
        print('Anna ist fertig')
        lock.release()

        print('Anna passt auf den Hund auf')


def paul():
    while True:
        sleep(randint(1, 10) / 10)
        print('Paul will schießen')

        lock.acquire()
        print('Paul geht schießen')
        sleep(randint(1, 10) / 10)
        print('Paul ist fertig')
        lock.release()

        print('Paul passt auf den Hund auf')


lock = Lock()

Thread(target=anna).start()
Thread(target=paul).start()
