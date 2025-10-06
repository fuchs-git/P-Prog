'''
Wechselseitiger Ausschluss - Mutex
der Begriff wechselseitiger Ausschluss bzw. Mutex (Abk. für englisch mutual exclusion) bezeichnet eine Gruppe
von Verfahren, mit denen das Problem des kritischen Abschnitts gelöst wird.
Wir nutzen das Threading Modul 'Lock'
'''

from threading import Thread, Lock
from time import sleep
from random import randint


def mensch(name):
    while True:
        sleep(randint(1, 10) / 10)
        print(f'{name} will schießen\n', end='')

        lock.acquire()
        print(f'{name} geht schießen\n', end='')
        sleep(randint(1, 10) / 10)
        print(f'{name} ist fertig\n', end='')
        lock.release()

        print(f'{name} passt auf den Hund auf\n', end='')


lock = Lock()
for name in ['Anna', 'Paul', 'John', 'Joe']:
    Thread(target=mensch, args=(name,)).start()
