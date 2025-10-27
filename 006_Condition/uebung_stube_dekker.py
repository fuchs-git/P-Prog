'''
Zwei Schüler, zwei Türen und ein Schild (wer das WC als letztes genutzt hat)
'''
from random import randint
from time import sleep
from threading import Thread, Condition
from typing import Any


class Tuer:
    def __init__(self):
        self.offen = True


class Schild:
    def __init__(self):
        self.schueler = None


class WC:
    def __init__(self, tuer_links: Tuer, tuer_rechts: Tuer):
        self.besetzt = False
        self.schild = Schild()
        self.tueren = [tuer_links, tuer_rechts]

    def gib_andere_Tuer(self, tuer: Tuer):
        return self.tueren[0] if tuer == self.tueren[1] else self.tueren[1]
        # if tuer == self.tueren[0]:
        #     return self.tueren[1]
        # return self.tueren[0]


class Schueler:
    def __init__(self, name: str, tuer: Tuer, wc: WC):
        self.name = name
        self.tuer = tuer
        self.wc = wc


tuer_links = Tuer()
tuer_rechts = Tuer()

wc = WC(tuer_links, tuer_rechts)

schueler1 = Schueler('Alice', tuer_links, wc)
schueler2 = Schueler('Bob', tuer_rechts, wc)

def job(schueler: Schueler):
    while True:
        # lernen
        print(schueler.name + ' lernt')
        sleep(randint(1,10)/10)

        # schueler.wc.gib_andere_Tuer(schueler.tuer).offen = False
        # schueler.tuer.offen = False

        # Dekker
        print(schueler.name + ' möchte das WC nutzen')
        andere_tuer = schueler.wc.gib_andere_Tuer(schueler.tuer)
        andere_tuer.offen = False
        while not schueler.tuer.offen:
            if wc.schild.schueler is schueler:
                andere_tuer = True
                while wc.schild.schueler is schueler:
                    pass
                andere_tuer.offen = False



        # WC benutzen
        sleep(randint(1, 10) / 10)
        print(schueler.name + ' nutzt das WC.')



        wc.schild.schueler = schueler
        schueler.wc.gib_andere_Tuer(schueler.tuer).offen = True
        schueler.tuer.offen = True
        print(schueler.name + ' verlässt das WC.')

Thread(target=job, args=(schueler1,)).start()
Thread(target=job, args=(schueler2,)).start()