"""
Drohnenstation mit Lock
"""
from threading import Thread, Lock
from time import sleep
from random import randint


class Plattform:
    def __init__(self):
        self.lock = Lock()  # gemeinsamer Zugangsschutz


class Drohne:
    def __init__(self, name: str, plattform: Plattform):
        self.name = name
        self.plattform = plattform

    def fliegen(self):
        while True:
            print(f'{self.name} fliegt umher.')
            sleep(randint(1, 10) / 10)
            print(f'{self.name} braucht Energie...')

            # Kritischer Abschnitt: nur eine Drohne darf laden
            self.laden()

            print(f'{self.name} verlässt die Plattform.\n')
            sleep(randint(1, 5) / 10)

    def laden(self):
        # Laden mit Lock-Steuerung innerhalb der Drohne
        with self.plattform.lock:  # automatisches acquire() und release()
            print(f'{self.name} landet auf der Plattform und lädt ⚡')
            sleep(randint(2, 5) / 10)
            print(f'{self.name} hat das Laden beendet.')


plattform = Plattform()

# Zwei Drohnen teilen sich die Plattform
d1 = Drohne("Drohne A", plattform)
d2 = Drohne("Drohne B", plattform)

Thread(target=d1.fliegen).start()
Thread(target=d2.fliegen).start()
