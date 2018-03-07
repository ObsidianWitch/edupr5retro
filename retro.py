import time
import tkinter
import PIL

class Clock:
    def __init__(self, framerate):
        self.period = (1 / framerate)
        self.timestart = time.time()

    def tick(self):
        delta = time.time() - self.timestart
        if (delta < self.period): time.sleep(self.period - delta)

        now = time.time()
        timepassed = now - self.timestart
        self.timestart = now

        return timepassed

class Window(tkinter.Tk):
    def __init__(self, title, size):
        self.size = size

        tkinter.Tk.__init__(self)
        self.title(title)

        self.canvas = tkinter.Canvas(
            self,
            width  = self.width,
            height = self.height,
            bg = "#000000",
        )
        self.canvas.pack()

    @property
    def width(self): return self.size[0]
    
    @property
    def height(self): return self.size[1]
