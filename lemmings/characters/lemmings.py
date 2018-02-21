import pygame

from lemmings.characters.lemming import Lemming
from shared.timer import Timer

# Lemming generator.
class Lemmings:
    def __init__(self, window, bg):
        self.window = window
        self.bg = bg

        self.group = pygame.sprite.Group()
        self.counter = 0
        self.max = 15
        self.timer = Timer(end = 15, period = 100)

    def generate(self):
        if (self.counter < self.max) and self.timer.finished:
            self.group.add(Lemming(self.window, self.bg))
            self.counter += 1
            self.timer.restart()

    def update(self, ui_action):
        self.generate()

        if not self.window.mousedown():
            self.group.update(False)
            return

        click = pygame.mouse.get_pos()
        for l in self.group:
            collision = l.rect.collidepoint(click)
            if collision: l.update(ui_action)
            else: l.update(False)

    def draw_bg(self):
        for l in self.group: l.draw_bg()
    def draw_screen(self):
        for l in self.group: l.draw_screen()
