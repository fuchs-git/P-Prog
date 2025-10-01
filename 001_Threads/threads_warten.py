from random import randint
from threading import Thread
from time import sleep

def job(zahl: int):
    sleep(randint(5,10))
    print('Thread', zahl, 'beendet.')

t1 = Thread(target=job, args=(1,))
t2 = Thread(target=job, args=(2,))

t1.start()
t2.start()

t1.join()
t2.join()
print('Beide Threads beendet.')