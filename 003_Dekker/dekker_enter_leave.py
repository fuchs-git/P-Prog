"""
Drohnenstation mit Dekker-Algorithmus (enter / leave Variante)
"""
from threading import Thread
from time import sleep
from random import randint


class Plattform:
    def __init__(self):
        self.flag_a = False
        self.flag_b = False
        self.turn = "A"  # wer hat Vorrang ("A" oder "B")

    def enter(self, thread_nr: int):
        if thread_nr == 0:  # Drohne A
            self.flag_a = True
            while self.flag_b:                   # B will auch laden?
                if self.turn == "B":             # B hat Vorrang?
                    self.flag_a = False          # A tritt zurück
                    while self.turn == "B":
                        pass                     # A wartet
                    self.flag_a = True

        else:  # Drohne B
            self.flag_b = True
            while self.flag_a:
                if self.turn == "A":
                    self.flag_b = False
                    while self.turn == "A":
                        pass
                    self.flag_b = True

    def leave(self, thread_nr: int):
        if thread_nr == 0:
            self.turn = "B"
            self.flag_a = False
        else:
            self.turn = "A"
            self.flag_b = False


class Drohne:
    def __init__(self, name: str, nummer: int, plattform: Plattform):
        self.name = name
        self.nr = nummer
        self.plattform = plattform

    def fliegen(self):
        while True:
            print(f"{self.name} fliegt umher.")
            sleep(randint(1, 10) / 10)
            print(f"{self.name} braucht Energie...")

            self.plattform.enter(self.nr)  # Eintritt in kritischen Abschnitt
            print(f"{self.name} landet auf der Plattform und lädt ⚡")
            sleep(randint(2, 5) / 10)
            print(f"{self.name} hat das Laden beendet.")
            self.plattform.leave(self.nr)  # Austritt aus kritischem Abschnitt

            print(f"{self.name} verlässt die Plattform.\n")
            sleep(randint(1, 5) / 10)


plattform = Plattform()

d1 = Drohne("Drohne A", 0, plattform)
d2 = Drohne("Drohne B", 1, plattform)

Thread(target=d1.fliegen).start()
Thread(target=d2.fliegen).start()