import random
import pygame

from shared.sprite import Sprite

class Fish:
    def __init__(self, window, sprite, speed, move):
        self.window = window
        self.sprite = sprite
        self.dx, self.dy = speed
        self.move = move

    def update(self):
        self.move(self)

    def flip(self, xflip = False, yflip = False):
        if xflip: self.dx *= -1
        if yflip: self.dy *= -1
        self.sprite.flip(xflip, False)

    # Moves from left to right.
    def move1(self):
        xnew = self.sprite.rect.x + self.dx

        limits = range(50, 3 * self.window.width // 4)
        if xnew not in limits: self.flip(xflip = True)

        self.sprite.rect.move_ip(self.dx, 0)

    # Moves diagonally.
    def move2(self):
        xnew = self.sprite.rect.x + self.dx
        ynew = self.sprite.rect.y + self.dy

        limits = lambda upper: range(20, upper - 100)
        if xnew not in limits(self.window.width):  self.flip(xflip = True)
        if ynew not in limits(self.window.height): self.flip(yflip = True)

        self.sprite.rect.move_ip(self.dx, self.dy)

    # Moves randomly.
    def move3(self):
        self.flip(
            xflip = (random.randrange(0, 100) == 0),
            yflip = (random.randrange(0, 100) == 0),
        )

        self.move2()
