from threading import Thread, Condition
from time import sleep

def test(i: int):
    with bedingung:
        # warten, bis ich an der Reihe bin
        warteschlange.append(i)
        while i != warteschlange[0]:
            bedingung.wait()

    # kritischer Abschnitt
    if i == 0:
        sleep(3)
    liste_danach.append(i)

    # Nächster darf rein
    with bedingung:
        warteschlange.pop(0)
        bedingung.notify_all()


bedingung = Condition()
liste_davor = list(range(1000))
liste_danach = []
warteschlange = []  # mutable, damit per Referenz geändert werden kann

threads = []
for i in liste_davor:
    threads.append(Thread(target=test, args=(i,)))

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print(liste_davor == liste_danach)
print(liste_davor[:20])  # zur Übersicht
print(liste_danach[:20])

# Parkhaus
def einfahren(self, auto: int):
    print(f'\r[+] Das Parkhaus hat {self.anzahl_freie_plaetze} freie Plätze', end='', flush=True)

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