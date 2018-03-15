import random
import include.retro as retro
from shared.sprite import Sprite

class Fish(Sprite):
    def __init__(self, window, path, speed, move):
        self.window = window
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

    # Moves from left to right.
    def move1(self):
        xnew = self.rect.x + self.dx

        limits = range(50, 3 * self.window.rect().w // 4)
        if xnew not in limits: self.flip(xflip = True)

        self.rect.move(self.dx, 0)

    # Moves diagonally.
    def move2(self):
        xnew = self.rect.x + self.dx
        ynew = self.rect.y + self.dy

        limits = lambda upper: range(20, upper - 100)
        if xnew not in limits(self.window.rect().w):  self.flip(xflip = True)
        if ynew not in limits(self.window.rect().h): self.flip(yflip = True)

        self.rect.move(self.dx, self.dy)

    # Moves randomly.
    def move3(self):
        self.flip(
            xflip = (random.randrange(0, 100) == 0),
            yflip = (random.randrange(0, 100) == 0),
        )

        self.move2()
