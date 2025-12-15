import time
import multiprocessing as mp

def ist_primzahl(x: int) -> bool:
    # die Funktion ist nicht sehr schlau, sondern absichtlich langsam!!!
    if x <= 1: return False
    for i in range(2, x):
        if x % i == 0: return False
    return True

if __name__ == '__main__':
    grenze = 50_000
    runs = (1, 2, 4, 8, 16, 32)  # Anzahl der Prozesse, die wir vorgeben

    for anzahl_prozesse in runs:
        ausgabe = f"{anzahl_prozesse:3} Prozesse:"

        start = time.time()
        with mp.Pool(anzahl_prozesse) as pool:  # with sorgt dafür, dass der Pool am Ende wieder aufgeräumt wird
            if anzahl_prozesse == 1:            # kein MP
                prim_oder_nicht = list(map(ist_primzahl, range(grenze)))
            else:
                prim_oder_nicht = list(pool.map(ist_primzahl, range(grenze)))
            zeit = time.time() - start
        print(f"Anzahl Prozesse:{anzahl_prozesse:3}, Anzahl gefundener Primzahlen: {prim_oder_nicht.count(True)}, Zeit: {zeit:6.2f} sec")

