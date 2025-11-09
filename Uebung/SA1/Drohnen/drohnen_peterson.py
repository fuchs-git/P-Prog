"""
Drohnenstation mit Peterson
"""

from random import randint
from threading import Thread
from time import sleep

class Plattform():
    def __init__(self):
        self.interested = [False, False]    # 0=DrohneA, 1=DrohneB
        self.turn = 0                       # Wer hat den Vorrang, wenn beide landen wollen

class Drohne:
    def __init__(self, name, plattform: Plattform, nummer: int):
        self.name = name
        self.plattform = plattform
        self.nummer = nummer

def enter_region(d: Drohne):
    other = 1 - d.nummer
    d.plattform.interested[d.nummer] = True
    d.plattform.turn = other
    while d.plattform.interested[other] and d.plattform.turn == other:
        pass

def leave_region(d: Drohne):
    d.plattform.interested[d.nummer] =False

def ladevorgang(drohne: Drohne):                    # Kritischer Bereich
    print(f'{drohne.name} ist am Laden ⚡\n', end='')
    sleep(randint(1, 10) / 10)

def job(d: Drohne):
    while True:
        print(f'{d.name} fliegt umher.\n', end='')
        sleep(randint(1, 10) / 10)

        print(f'{d.name} braucht Energie...\n', end='')
        enter_region(d)
        ladevorgang(d)
        leave_region(d)

        print(f'{d.name} verlässt die Plattform\n', end='')
        sleep(randint(1, 5) / 10)

plattform = Plattform()
d1 = Drohne("Drohne A", plattform, 0)
d2 = Drohne("Drohne B", plattform, 1)

Thread(target=job, args=(d1,)).start()
Thread(target=job, args=(d2,)).start()