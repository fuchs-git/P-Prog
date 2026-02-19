import typing
from typing import Any, Union
import time, random
from threading import Thread


class Liste:
    class _Wagon:
        def __init__(self, value):
            self.next = None
            self.value = value

        def __repr__(self):
            return repr(self.value)

    # ab hier die Listeninterna

    def __init__(self, dinge:typing.Iterable=None):
        self._first = None
        if dinge is not None:
            self.extend(dinge)

    def __contains__(self, item):  # nativer Support für den "in"-Operator (ohne Fallback auf iter oder getitem)
        for elem in self:
            if elem == item:
                return True
        return False

    def __iter__(self):  # Generator-Methode, nativer Support von Iteration via iter/next (ohne Fallback auf getitem)
        wagon = self._first
        while wagon is not None:
            yield wagon.value
            wagon = wagon.next

    def __getitem__(self, index):  # indizierter lesender Zugriff
        if type(index) is not int:
            raise TypeError("Index muss ein int sein")
        if index < 0 or self._first is None:  # index negativ oder Liste leer
            raise IndexError("list index out of range")  # das ist die kopierte Meldung der Python-Liste

        schaffner = self._first
        while index > 0:
            schaffner = schaffner.next
            if schaffner is None:
                raise IndexError("list index out of range")
            index -= 1
        return schaffner.value

    def __len__(self) -> int:  # len
        if self._first is None:
            return 0
        else:
            schaffner = self._first
            counter = 1
            while schaffner.next is not None:
                schaffner = schaffner.next
                counter += 1
            return counter

    def __repr__(self):  # repr und str
        if self._first is None:
            return "[]"
        ergebnis = repr(self._first)
        schaffner = self._first
        while schaffner.next is not None:
            schaffner = schaffner.next
            ergebnis += f", {repr(schaffner)}"
        return f"[{ergebnis}]"

    def __setitem__(self, index: int, wert: Any) -> None: # indizierter schreibender Zugriff
        if type(index) is not int:
            raise TypeError("Index muss ein int sein")
        if index < 0 or self._first is None:  # index negativ oder Liste leer
            raise IndexError("list index out of range")  # das ist die kopierte Meldung der Python-Liste
        schaffner = self._first
        while index > 0:
            schaffner = schaffner.next
            if schaffner is None:
                raise IndexError("list index out of range")
            index -= 1
        schaffner.value = wert

    def append(self, value: Any):
        if self._first is None:
            self._first = Liste._Wagon(value)
        else:
            schaffner = self._first
            while schaffner.next is not None:
                schaffner = schaffner.next
            neu = Liste._Wagon(value)
            schaffner.next = neu

    def copy(self):  # Version ohne append
        kopie = Liste()
        schaffner_original = self._first
        if schaffner_original is not None:  # den ersten Wagen an die neue Lok hängen
            kopie._first = Liste._Wagon(schaffner_original.value)
            schaffner_kopie = kopie._first
            schaffner_original = schaffner_original.next
            while schaffner_original is not None:  # alle weiteren Wagen anhängen
                schaffner_kopie.next = Liste._Wagon(
                    schaffner_original.value)  # value wird nur "shallow" kopiert, nicht "deep"
                schaffner_kopie = schaffner_kopie.next
                schaffner_original = schaffner_original.next
        return kopie

    def extend(self, ding:typing.Iterable):
        # man muss unterscheiden, ob die Liste noch leer ist oder nicht und in dem Fall das erste Einfügen anders machen
        # daher hier mal mit iter und next, da lässt sich das Konzept nochmal schön zeigen
        ding_iter = iter(ding)
        try:
            elem = next(ding_iter) # sollte das Ding leer sein, hört es hier schon wieder auf
            if self._first is None:
                aktuell = self._Wagon(elem)
                self._first=aktuell
            else:
                aktuell = self._first
                while aktuell.next is not None:
                    aktuell = aktuell.next
                aktuell.next = self._Wagon(elem)
                aktuell = aktuell.next
            while True: # aus der Schleife kommen wir mit StopIteration raus
                aktuell.next = self._Wagon(next(ding_iter))
                aktuell = aktuell.next
        except StopIteration:
            pass

    def sort_bubble(self):
        '''
        wie das "normale" Bubblesort, statt aber in jedem Schritt jeweils explizit zu prüfen, ob das Listenende
        erreicht ist, wird macnhmal stumpf immer weiter gemacht, bis ein Fehler geworfen wird. Das funktioniert auch
        und spart ggf. Zeit (hier bei uns spart es ein ganz klein wenig Zeit im einstelligen Prozent-Bereich)
        :return: nix, sortiert in-place
        '''
        swapped = True
        while swapped:
            swapped = False
            schaffner1 = self._first
            if schaffner1 is not None:
                schaffner2 = schaffner1.next
                try:
                    while True:
                        if schaffner1.value > schaffner2.value:
                            schaffner1.value, schaffner2.value = schaffner2.value, schaffner1.value
                            swapped = True
                        schaffner1 = schaffner2
                        schaffner2 = schaffner2.next
                except (TypeError, AttributeError):
                    pass

    def sort_bubble_array(self):
        '''
        Bubblesort mit direkter Indizierung, so, als ob unsere Liste ein Array wäre
        Dadurch kann man den Standard-Algorithmus direkt hier umsetzen
        es wird funktionieren, es wird aber schrecklich langsam sein!!!
        erfordert __getitem__ und __setitem__ damit die lesenden und schreibenden Zugriffe per Index möglich sind
        :return: nix, sortiert in-place
        '''
        n = len(self)
        swapped = True
        while swapped:  # wurde im letzten Durchlauf getauscht? (auch das ist schon eine Optimierung)
            swapped = False
            for i in range(1, n):  # ein Durchlauf aller Paare
                if self[i - 1] > self[i]:  # größeres vor kleinerem?
                    self[i - 1], liste[i] = self[i], self[i - 1]  # tauschen
                    swapped = True
            n -= 1  # Optimierung (fertig sortierte Elemente am oberen Ende werden nicht erneut betrachtet)


    def sort_quick(self):
        """
        in-place Quicksort das nur tauscht (kein zusätzliches Array, kein Umhängen von Wagons)
        den Platz auf dem Aufruf-Stack braucht man natürlich trotzdem
        schnell auf zufälligen Listen
        nicht stabil
        nicht für Grenzfälle geeignet (z.B. vorsortierte Liste) (dann ist es unnötig langsam oder ganz kaputt)
        :return:  nix, in-place
        """
        def quicksort(links, rechts, tiefe):
            if links is rechts: return
            pivot = links.value  # Pivot
            aktuell = links  # aktuell Untersuchter
            vorgrenze = links  # Vorgänger von Obergrenze
            grenze = links  # Oberster, der kleiner/gleich dem Pivot ist
            while True:
                aktuell = aktuell.next
                if aktuell is rechts: break
                if aktuell.value < pivot:
                    vorgrenze = grenze
                    grenze = grenze.next
                    grenze.value, aktuell.value = aktuell.value, grenze.value
            links.value, grenze.value = grenze.value, links.value
            if grenze is not rechts:
                vorgrenze = grenze
                grenze = grenze.next

            if tiefe > 0:
                threads = [
                Thread(target=quicksort, args=(links, vorgrenze, tiefe-1)),
                Thread(target=quicksort, args=(grenze, rechts, tiefe-1))
                    ]

                for thread in threads:
                    thread.start()
                for thread in threads:
                    thread.join()

            else:
                quicksort(links, vorgrenze, 0)
                quicksort(grenze, rechts, 0)

        quicksort(self._first, None, tiefe=3)

    def unique(self):
        """
        ©️Beesten
        in-place, entfernt doppelt auftretende Elemente
        :return: nichts, es wird dir originale Liste (self) verändert
        """
        schaffner = self._first
        while schaffner is not None:
            vorgaenger = schaffner
            kontroletti = schaffner.next
            while kontroletti is not None:
                nachfolger = kontroletti.next
                if kontroletti.value == schaffner.value:
                    vorgaenger.next = nachfolger
                else:
                    vorgaenger = kontroletti
                kontroletti = nachfolger
            schaffner = schaffner.next
        return


if __name__ == '__main__':  # lokaler test

    for n in (1_000,10_000, 100_000): # , 100_000, 1_000_000
        print(f"\n{n:_} random Elemente werden sortiert")

        liste_python = [random.randint(0,n) for _ in range(n)]
        liste_linked_quick = Liste(liste_python)

        start = time.time()
        liste_python.sort()
        print(f"PowerSort auf Python-Liste: {time.time()-start:10.7f}sec",)

        start = time.time()
        liste_linked_quick.sort_quick()
        print(f"QuickSort auf Linked-Liste: {time.time()-start:10.7f}sec",)


        assert str(liste_linked_quick) == str(liste_python)


    for n in (100,995 ): # 995, 1000, 100_000
        print(f"\n{n:_} vorsortierte Elemente werden sortiert")

        liste_python = [x for x in range(n)]
        liste_linked_quick = Liste(liste_python)

        start = time.time()
        liste_python.sort()
        print(f"PowerSort auf Python-Liste: {time.time()-start:10.7f}sec",)

        start = time.time()
        try:
            liste_linked_quick.sort_quick()
        except RecursionError:
            print(f"QuickSort auf Linked-Liste:  Error",)
        else:
            print(f"QuickSort auf Linked-Liste: {time.time()-start:10.7f}sec",)


        assert str(liste_linked_quick) == str(liste_python)

