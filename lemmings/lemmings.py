import pygame

from shared.timer import Timer
from lemmings.lemming import Lemming

class Lemmings:
    def __init__(self, window):
        self.window = window

        self.group = pygame.sprite.Group()
        self.counter = 0
        self.max = 15
        self.timer = Timer(end = 15, period = 100)

    def generate(self):
        if (self.counter < self.max) and self.timer.finished:
            self.group.add(Lemming(self.window))
            self.counter += 1
            self.timer.restart()

    def update(self): self.group.update()

    def draw(self): self.group.draw(self.window.screen)
