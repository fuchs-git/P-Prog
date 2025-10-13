'''
Wechselseitiger Ausschluss - mit einer Condition
'''

from threading import Thread, Condition
from time import sleep
from random import randint


def job(name):
    global schiessbahn_frei

    # blocken der Ressource
    with condition:
        while not schiessbahn_frei:
            condition.wait()
        schiessbahn_frei = False

    #  kritischer Bereich
    liste_danach.append(name)
    if name == 0:
        sleep(5)

    # freigabe der Ressource
    with condition:
        schiessbahn_frei = True
        condition.notify()


condition = Condition()
schiessbahn_frei = True

liste_davor = list(range(1000))
liste_danach = []

threads = []

for i in liste_davor:
    threads.append(Thread(target=job, args=(i,)))

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print(liste_davor == liste_danach)
print(liste_davor)
print(liste_danach)
