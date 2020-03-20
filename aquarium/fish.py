import random
from retro.src import retro

class Fish(retro.Sprite):
    def __init__(self, path, speed):
        image = retro.Image.from_path(path)
        retro.Sprite.__init__(self, [image])
        self.dx, self.dy = speed

    def flip(self, xflip = False, yflip = False):
        if xflip: self.dx *= -1
        if yflip: self.dy *= -1
        self.image.flip(xflip, False)

    # Moves from left to right, constrained by `target.rect`.
    def move1(self, target):
        xnew = self.rect.x + self.dx

        limits = range(50, 3 * target.rect().w // 4)
        if xnew not in limits: self.flip(xflip = True)

        self.rect.move_ip(self.dx, 0)

    # Moves diagonally, constrained by `target.rect`.
    def move2(self, target):
        xnew = self.rect.x + self.dx
        ynew = self.rect.y + self.dy

        limits = lambda upper: range(20, upper - 100)
        if xnew not in limits(target.rect().w):  self.flip(xflip = True)
        if ynew not in limits(target.rect().h): self.flip(yflip = True)

        self.rect.move_ip(self.dx, self.dy)

    # Moves randomly, constrained by `target.rect`.
    def move3(self, target):
        self.flip(
            xflip = (random.randrange(0, 100) == 0),
            yflip = (random.randrange(0, 100) == 0),
        )
        self.move2(target)
