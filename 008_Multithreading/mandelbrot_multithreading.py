import tkinter as tk
import math
from time import time
from threading import Thread


class MandelbrotApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Mandelbrot-Fraktal")
        self.width = 800
        self.height = 600
        self.max_iter = 200
        self.xmin, self.xmax = -2.5, 1.0
        self.ymin, self.ymax = -1.5, 1.5 * (self.height / self.width)
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.img = tk.PhotoImage(width=self.width, height=self.height)
        self.canvas_image = self.canvas.create_image(0, 0, image=self.img, anchor="nw")
        self.sel_rect = None
        self.start_xy = None
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.render()

    def render(self):
        def job(start, ende):
            for y in range(start, ende):
                cy = ymin + (y / (h - 1)) * (ymax - ymin)
                row_colors = []
                for x in range(w):
                    cx = xmin + (x / (w - 1)) * (xmax - xmin)
                    zx, zy = 0.0, 0.0
                    it = 0
                    while zx * zx + zy * zy <= 4.0 and it < self.max_iter:
                        x_new = zx * zx - zy * zy + cx
                        zy = 2.0 * zx * zy + cy
                        zx = x_new
                        it += 1
                    color = self.color_map(it, self.max_iter, zx, zy)
                    row_colors.append(color)
                rows[y] = "{" + " ".join(row_colors) + "}"


        w, h = self.width, self.height
        xmin, xmax = self.xmin, self.xmax
        ymin, ymax = self.ymin, self.ymax
        rows = ['' for y in range(h)]

        startzeit = time()

        anzahl_threads = 2
        threads = []
        for i in range(anzahl_threads):
            start = (h // anzahl_threads) * i
            ende = (h // anzahl_threads) * (i + 1)
            threads.append(Thread(target=job, args=(start, ende)))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        for y in range(h):
            self.img.put(rows[y], to=(0, y))

        print('Zeit:', time()-startzeit)
        # Diese Schleife verursacht die Auslastung der CPU

    def color_map(self, it, max_iter, zx, zy):
        if it >= max_iter:
            return "#000000"
        r2 = zx * zx + zy * zy
        if r2 > 0.0:
            smooth = it - math.log(math.log(r2)) / math.log(2)
        else:
            smooth = float(it)
        t = max(0.0, min(1.0, smooth / max_iter))
        r = int(127.5 * (1 + math.sin(6.3 * t + 0.0)))
        g = int(127.5 * (1 + math.sin(6.3 * t + 2.1)))
        b = int(127.5 * (1 + math.sin(6.3 * t + 4.2)))
        return f"#{r:02x}{g:02x}{b:02x}"

    def reset_view(self):
        self.xmin, self.xmax = -2.5, 1.0
        self.ymin, self.ymax = -1.5, 1.5 * (self.height / self.width)
        self.render()

    def on_mouse_down(self, event):
        self.start_xy = (event.x, event.y)
        if self.sel_rect is not None:
            self.canvas.delete(self.sel_rect)
            self.sel_rect = None

    def on_mouse_drag(self, event):
        if not self.start_xy:
            return
        x0, y0 = self.start_xy
        x1, y1 = event.x, event.y
        if self.sel_rect is None:
            self.sel_rect = self.canvas.create_rectangle(x0, y0, x1, y1, outline="white", width=1, dash=(4, 2))
        else:
            self.canvas.coords(self.sel_rect, x0, y0, x1, y1)

    def on_mouse_up(self, event):
        if not self.start_xy:
            return
        x0, y0 = self.start_xy
        x1, y1 = event.x, event.y
        self.start_xy = None
        if self.sel_rect is not None:
            self.canvas.delete(self.sel_rect)
            self.sel_rect = None
        if abs(x1 - x0) < 5 or abs(y1 - y0) < 5:
            return
        xa, xb = sorted((x0, x1))
        ya, yb = sorted((y0, y1))
        new_xmin = self.xmin + (xa / (self.width - 1)) * (self.xmax - self.xmin)
        new_xmax = self.xmin + (xb / (self.width - 1)) * (self.xmax - self.xmin)
        new_ymin = self.ymin + (ya / (self.height - 1)) * (self.ymax - self.ymin)
        new_ymax = self.ymin + (yb / (self.height - 1)) * (self.ymax - self.ymin)
        self.xmin, self.xmax = new_xmin, new_xmax
        self.ymin, self.ymax = new_ymin, new_ymax
        self.render()


app = MandelbrotApp()
app.mainloop()
