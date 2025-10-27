'''
Zwei Schüler, zwei Türen und ein Schild (wer das WC als letztes genutzt hat)
'''

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
