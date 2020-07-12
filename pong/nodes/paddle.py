import enum
from retro.src import retro

class Paddle:
    SIDE = enum.Enum("SIDE", "LEFT RIGHT")

    def __init__(self, window, side):
        self.window = window
        self.side = side
        self.rect = retro.Rect(0, 0, 10, 50)

        offset = 20
        if side == self.SIDE.LEFT:
            self.rect.left = offset
        elif side == self.SIDE.RIGHT:
            self.rect.right = window.rect().w - offset
        self.rect.centery = window.rect().h // 2

        self.dy = 4
        self.score = 0

    def move(self):
        key = self.window.events.key_hold
        if self.side == self.SIDE.LEFT:
            if key(retro.K_UP):   self.rect.y -= self.dy
            if key(retro.K_DOWN): self.rect.y += self.dy
        elif self.side == self.SIDE.RIGHT:
            if key(retro.K_q): self.rect.y -= self.dy
            if key(retro.K_a): self.rect.y += self.dy

    def walls_collision(self):
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.window.rect().h:
            self.rect.bottom = self.window.rect().h

    def update(self):
        self.move()
        self.walls_collision()

    def draw(self):
        self.window.draw_rect(
            color = retro.WHITE,
            rect  = self.rect,
        )
