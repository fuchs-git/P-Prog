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

    # def betreten(self, schueler: 'Schueler'):
    #     pass
    #
    # def verlassen(self, schueler: 'Schueler'):
    #     pass


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

        # Peterson - kritischer Bereich
        print(schueler.name + ' möchte das WC nutzen')
        andere_tuer = schueler.wc.gib_andere_Tuer(schueler.tuer)
        andere_tuer.offen = False
        schueler.wc.schild.schueler = schueler
        while not schueler.tuer.offen and schueler.wc.schild.schueler is not schueler:
            pass



        # WC benutzen
        sleep(randint(1, 10) / 10)
        print(schueler.name + ' nutzt das WC.')


        andere_tuer.offen = True
        print(schueler.name + ' verlässt das WC.')

Thread(target=job, args=(schueler1,)).start()
Thread(target=job, args=(schueler2,)).start()