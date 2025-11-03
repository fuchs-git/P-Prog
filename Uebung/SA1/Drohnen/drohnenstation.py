"""
drohnenstation.py
Fehlerhafte Ausgangsdatei zur Schulaufgabe Parallele Programmierung
Simulation: Zwei Drohnen teilen sich eine Landeplattform
"""

import threading
import time
import random


class Plattform:
    def __init__(self):
        self.frei = True  # Plattform ist anfangs frei


class Drohne(threading.Thread):
    def __init__(self, name: str, plattform: Plattform):
        super().__init__()
        self.name = name
        self.plattform = plattform

    def run(self):
        while True:
            print(f"{self.name} fliegt ihre Runde im Luftraum …")
            time.sleep(random.uniform(0.2, 0.6))

            print(f"{self.name} möchte landen …")
            # ❌ FEHLER: keine Synchronisation — beide Drohnen können gleichzeitig landen!
            if self.plattform.frei:
                print(f"{self.name} landet auf der Plattform.")
                self.plattform.frei = False
                time.sleep(random.uniform(0.3, 0.6))
                print(f"{self.name} startet wieder.")
                self.plattform.frei = True
            else:
                print(f"{self.name} muss warten – Plattform ist belegt.")

            time.sleep(random.uniform(0.2, 0.5))


if __name__ == "__main__":
    plattform = Plattform()
    d1 = Drohne("Drohne A", plattform)
    d2 = Drohne("Drohne B", plattform)

    d1.start()
    d2.start()