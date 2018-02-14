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
        self.sprite.image = pygame.transform.flip(
            self.sprite.image, xflip, False
        )

    # Move from left to right.
    def move1(self):
        xnew = self.sprite.rect.x + self.dx

        if not (50 <= xnew <= 3 * self.window.width // 4):
            self.flip(xflip = True)

        self.sprite.rect.move_ip(self.dx, 0)

    # Move diagonally.
    def move2(self):
        xnew = self.sprite.rect.x + self.dx
        ynew = self.sprite.rect.y + self.dy

        if not (20 <= xnew <= self.window.width -100):
            self.flip(xflip = True)
        if not (20 <= ynew <= self.window.height -100):
            self.flip(yflip = True)

        self.sprite.rect.move_ip(self.dx, self.dy)

    # Move randomly.
    def move3(self):
        self.flip(
            xflip = (random.randint(0, 100) == 0),
            yflip = (random.randint(0, 100) == 0)
        )

        self.move2()
