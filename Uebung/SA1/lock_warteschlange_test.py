from threading import Thread, Lock
from time import sleep


def test(i: int):
    lock.acquire()
    if i == 0: sleep(3)
    liste_danach.append(i)
    lock.release()


lock = Lock()
liste_davor = list(range(1000))
liste_danach = []


threads = []
for i in liste_davor:
    threads.append(Thread(target=test, args=(i,)))

for thread in threads:
    thread.start()
    sleep(0.01)

for thread in threads:
    thread.join()

print(liste_davor == liste_danach)
print(liste_davor)
print(liste_danach)