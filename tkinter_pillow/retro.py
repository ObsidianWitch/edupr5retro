import time
import tkinter
import PIL

class Clock:
    def __init__(self, framerate):
        self.period = (1 / framerate)
        self.last_tick = time.time()

    def tick(self):
        delta = time.time() - self.last_tick
        if (delta < self.period): time.sleep(self.period - delta)

        now = time.time()
        time_passed = now - self.last_tick
        self.last_tick = now

        return time_passed

class Window(tkinter.Tk):
    def __init__(self, title, size):
        self.size = size

        tkinter.Tk.__init__(self)
        self.title(title)

        self.canvas = tkinter.Canvas(
            self,
            width  = self.width,
            height = self.height,
            bg     = "#000000",
        )
        self.canvas.pack()

        self.screen = self.canvas.create_image((0, 0), anchor = tkinter.NW)

        self.buffer = PIL.Image.new('RGBA', self.size)

    @property
    def width(self): return self.size[0]

    @property
    def height(self): return self.size[1]

    def draw(self):
        # Transfert de la zone de dessin vers l'ecran
        buffertk = PIL.ImageTk.PhotoImage(self.buffer)
        self.canvas.itemconfig(self.screen, image = buffertk)

        # Affichage
        self.canvas.update()
