import random
import shared.retro as retro
from shared.sprite import Sprite

class Fish(Sprite):
    def __init__(self, path, speed, move):
        sprite = retro.Image.from_path(path)
        Sprite.__init__(self, sprite)
        self.dx, self.dy = speed
        self.move = move

    def update(self):
        self.move(self)

    def flip(self, xflip = False, yflip = False):
        if xflip: self.dx *= -1
        if yflip: self.dy *= -1
        Sprite.flip(self, xflip, False)

    # Moves from left to right, constrained by `rect`.
    def move1(self, rect):
        xnew = self.rect.x + self.dx

        limits = range(50, 3 * rect.w // 4)
        if xnew not in limits: self.flip(xflip = True)

        self.rect.move(self.dx, 0)

    # Moves diagonally, constrained by `rect`.
    def move2(self, rect):
        xnew = self.rect.x + self.dx
        ynew = self.rect.y + self.dy

        limits = lambda upper: range(20, upper - 100)
        if xnew not in limits(rect.w):  self.flip(xflip = True)
        if ynew not in limits(rect.h): self.flip(yflip = True)

        self.rect.move(self.dx, self.dy)

    # Moves randomly, constrained by rect.
    def move3(self, rect):
        self.flip(
            xflip = (random.randrange(0, 100) == 0),
            yflip = (random.randrange(0, 100) == 0),
        )
        self.move2(rect)
