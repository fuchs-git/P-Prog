import tkinter as tk
from threading import Thread
from time import sleep, time

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.zeit_label = tk.Label(self, text='', width=20)
        self.zeit_label.pack(side=tk.LEFT)
        self.button = tk.Button(self, text='Start', command=self.klick, width=10)
        self.button.pack(side=tk.LEFT)
        self.running = False
        self.mainloop()

    def klick(self):
        self.running = not self.running
        if self.running:
            Thread(target=self.job).start()
            self.button.config(text='Abbrechen')
        else:
            self.button.config(text='Start')

    def job(self):
        while self.running: # Thread beendet sich
            self.zeit_label.config(text=f'{time():.0f}')
            sleep(1)

App()