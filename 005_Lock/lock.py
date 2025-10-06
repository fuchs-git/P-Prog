'''
Wechselseitiger Ausschluss - Mutex
der Begriff wechselseitiger Ausschluss bzw. Mutex (Abk. für englisch mutual exclusion) bezeichnet eine Gruppe
von Verfahren, mit denen das Problem des kritischen Abschnitts gelöst wird.
Wir nutzen das Threading Modul 'Lock'
'''

from threading import Thread, Lock
from time import sleep
from random import randint

def job(thread_nummer):
    while True:
        sleep(randint(1,10)/10)
        lock.acquire()
        print('Thread', thread_nummer, 'betritt kritischen Abschnitt')
        sleep(randint(1,10)/10)
        print('Thread', thread_nummer, 'verlässt kritischen Abschnitt')
        lock.release()

lock = Lock()

Thread(target=job, args=(0,)).start()
Thread(target=job, args=(1,)).start()


