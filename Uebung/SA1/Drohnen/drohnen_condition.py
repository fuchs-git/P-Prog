"""
Drohnenstation mit Condition()
"""
from threading import Thread, Condition
from time import sleep
from random import randint


class Plattform:
    def __init__(self):
        # Condition kombiniert Lock + Warteschlange
        self.condition = Condition()
        self.besetzt = False  # Plattformstatus

    def betreten(self, drohne_name: str):
        # Wird aufgerufen, wenn eine Drohne landen möchte
        with self.condition:
            while self.besetzt:
                print(f'⏳ {drohne_name} wartet auf freie Plattform...\n', end='')
                self.condition.wait()  # warten, bis notify() gesendet wird
            self.besetzt = True
            print(f'{drohne_name} landet auf der Plattform und lädt ⚡\n', end='')

    def verlassen(self, drohne_name: str):
        # Wird aufgerufen, wenn eine Drohne fertig ist
        with self.condition:
            self.besetzt = False
            print(f'{drohne_name} verlässt die Plattform.\n', end='')
            self.condition.notify()  # signalisiert: Plattform wieder frei


class Drohne:
    def __init__(self, name: str, plattform: Plattform):
        self.name = name
        self.plattform = plattform

    def fliegen(self):
        while True:
            print(f'{self.name} fliegt umher.\n', end='')
            sleep(randint(1, 10) / 10)
            print(f'{self.name} braucht Energie...\n', end='')
            self.laden()
            sleep(randint(1, 5) / 10)

    def laden(self):
        # Laden mit Condition-gesteuerter Plattform
        self.plattform.betreten(self.name)
        sleep(randint(2, 5) / 10)
        print(f'{self.name} hat das Laden beendet.\n', end='')
        self.plattform.verlassen(self.name)


# --- Start ---
plattform = Plattform()

d1 = Drohne("Drohne A", plattform)
d2 = Drohne("Drohne B", plattform)
d3 = Drohne("Drohne C", plattform)

Thread(target=d1.fliegen).start()
Thread(target=d2.fliegen).start()
Thread(target=d3.fliegen).start()
