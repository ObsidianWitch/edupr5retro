from shared.timer import Timer

from lemmings.lemming  import Lemming

class Lemmings:
    def __init__(self, window):
        self.window = window

        self.lst = []
        self.max = 15
        self.timer = Timer(end = 15, period = 100)

    def generate(self):
        if (len(self.lst) < self.max) and self.timer.finished:
            self.lst.append(Lemming(self.window))
            self.timer.restart()

    def update(self):
        for lemming in self.lst: lemming.update()

    def draw(self):
        for lemming in self.lst: lemming.draw()
