from threading import Thread
from time import sleep

def job():
    for i in range(10)[:0:-1]:
        print(i)
        sleep(1)
    print('boom...')

Thread(target=job).start()
Thread(target=job).start()
print('Thread gestartet...')
print('Bin fertig...')

