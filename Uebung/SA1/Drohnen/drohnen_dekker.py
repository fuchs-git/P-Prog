"""
Drohnenstation mit Dekker
"""
from random import randint
from threading import Thread
from time import sleep


class Plattform:
    def __init__(self):
        self.frei = True          # rein symbolisch
        self.log = "Drohne A"     # = turn (wer hat Vorrang)
        self.flag_a = False       # Drohne A will laden
        self.flag_b = False       # Drohne B will laden


class Drohne:
    def __init__(self, name: str, plattform: Plattform):
        self.name = name
        self.plattform = plattform
        self.energie = True


def job(drohne: Drohne):
    while True:
        print(f'{drohne.name} fliegt umher.\n', end='')
        sleep(randint(1, 10) / 10)

        print(f'{drohne.name} braucht Energie')

        # ------------------- Dekker-Algorithmus -------------------
        if drohne.name == "Drohne A":
            drohne.plattform.flag_a = True
            while drohne.plattform.flag_b:                 # B will auch laden?
                if drohne.plattform.log == "Drohne A":     # hat A als letztes geladen
                    drohne.plattform.flag_a = False        # -> A tritt zurück
                    while drohne.plattform.log == "Drohne A":
                        pass
                    drohne.plattform.flag_a = True
            # ----- kritischer Abschnitt -----
            ladevorgang(drohne)
            drohne.plattform.log = "Drohne A"              # A war als letztes dran
            drohne.plattform.flag_a = False

        else:  # Drohne B
            drohne.plattform.flag_b = True
            while drohne.plattform.flag_a:
                if drohne.plattform.log == "Drohne B":
                    drohne.plattform.flag_b = False
                    while drohne.plattform.log == "Drohne B":
                        pass
                    drohne.plattform.flag_b = True
            # ----- kritischer Abschnitt -----
            ladevorgang(drohne)
            drohne.plattform.log = "Drohne B"           # B war als letztes dran
            drohne.plattform.flag_b = False
        # -----------------------------------------------------------

        print(f'{drohne.name} verlässt die Plattform\n', end='')
        sleep(randint(1, 5) / 10)


def ladevorgang(drohne: Drohne):
    drohne.plattform.frei = False
    print(f'{drohne.name} ist am Laden ⚡\n', end='')
    sleep(randint(1, 10) / 10)
    drohne.plattform.frei = True


# --- Start ---
plattform = Plattform()
d1 = Drohne("Drohne A", plattform)
d2 = Drohne("Drohne B", plattform)

Thread(target=job, args=(d1,)).start()
Thread(target=job, args=(d2,)).start()