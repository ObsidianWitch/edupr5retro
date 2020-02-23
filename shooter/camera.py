import shared.retro as retro
from shared.directions import Directions

class Camera:
    def __init__(self, window, bg, position):
        self.window = window
        self.bg = bg

        self.rect = window.rect()
        self.rect.move(position)

        self.speed = 10

    def bg_space(self, p): return (
        p[0] + self.rect.x,
        p[1] + self.rect.y,
    )
