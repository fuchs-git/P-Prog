from threading import Thread

def job():
    global zahl
    for i in range(1000):
        z = zahl
        for i in range(10001):
            z += 1
        for i in range(10000):
            z -= 1
        zahl = z

zahl = 0

t1 = Thread(target=job)
t2 = Thread(target=job)

t1.start()
t2.start()

t1.join()
t2.join()
print('Summe', zahl)