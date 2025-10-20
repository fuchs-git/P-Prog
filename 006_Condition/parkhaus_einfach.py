'''
Beispiel eines Parkhauses für das nutzen einer Condition
'''

from threading import Thread, Condition
from time import sleep
from random import randint
from typing import Any


class Parkhaus:

    wartende_autos: list[Any]

    def __init__(self, anzahl_plaetze: int):
        self.anzahl_freie_plaetze = anzahl_plaetze
        self.wartende_autos = []
        self.condition = Condition()

    def einfahren(self, auto: int):
        print(f'\r[+] Das Parkhaus hat {self.anzahl_freie_plaetze} freie Plätze',end='', flush=True)

        with self.condition:
            self.wartende_autos.append(auto)
            while self.wartende_autos[0] is not auto or self.anzahl_freie_plaetze <= 0:
                self.condition.wait()

            self.wartende_autos.pop(0)
            self.anzahl_freie_plaetze -= 1

    def ausfahren(self):
        with self.condition:
            self.anzahl_freie_plaetze += 1
            self.condition.notify_all()


def auto(nummer):
    while True:
        sleep(randint(1,10)/10)

        # print(f'Auto {nummer} will parken\n', end='')
        augsburg_allee.einfahren(nummer)
        # print(f'Auto {nummer} parkt\n', end='')
        sleep(randint(1,10)/10)
        # print(f'Auto {nummer} fährt raus\n', end='')
        augsburg_allee.ausfahren()




augsburg_allee = Parkhaus(70)

besucher = []
for i in range(100):
    Thread(target=auto, args=(i,)).start()


