def merge_sort(self):
    def merge_help(start: Liste._Wagon, stop: Liste._Wagon, ergebnisliste: list, index: int) -> Liste._Wagon:
        global counter
        global lock
        if start is stop:
            ergebnisliste[index] = None
            return
        if start.next is stop:
            start.next = None
            ergebnisliste[index] = start
            return

        # teile die Liste in der Mitte...
        temp = start
        temp2 = start
        while temp2 is not stop and temp2.next is not stop:
            temp = temp.next
            temp2 = temp2.next.next

        lock.acquire()
        teillisten = [None, None]

        if counter < 16:
            counter += 2
            lock.release()

            threads = [
                Thread(target=merge_help, args=(start, temp, teillisten, 0)),
                Thread(target=merge_help, args=(temp, stop, teillisten, 1)),
            ]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

            lock.acquire()
            counter -= 2
            lock.release()

        else:
            lock.release()
            merge_help(start, temp, teillisten, 0)
            merge_help(temp, stop, teillisten, 1)

        links = teillisten[0]
        rechts = teillisten[1]

        # merge
        ret = None  # Anfang der zurückzugebenden Wagonkette
        if links.value < rechts.value:
            ret = links
            links = links.next
        else:
            ret = rechts
            rechts = rechts.next
        temp = ret

        while links is not None and rechts is not None:
            if links.value < rechts.value:
                temp.next = links
                links = links.next
            else:
                temp.next = rechts
                rechts = rechts.next
            temp = temp.next
        if rechts is None:
            temp.next = links
        else:
            temp.next = rechts

        ergebnisliste[index] = ret
        return

    ergebnis = [None]
    merge_help(self._first, None, ergebnis, 0)
    self._first = ergebnis[0]