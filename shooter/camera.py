import shared.retro as retro
from shared.directions import Directions

class Camera:
    def __init__(self, window, bg, position):
        self.window = window
        self.bg = bg

        self.camera_space = window.rect()
        self.camera_space.move(position)

        self.speed = 10

    def scroll_vec(self, p):
        offset = 20
        w = self.window.rect().w
        h = self.window.rect().h
        return Directions(
            up    = (0 <= p[1] <= offset),
            down  = (h - offset <= p[1] <= h),
            left  = (0 <= p[0] <= offset),
            right = (w - offset <= p[0] <= w),
        ).vec

    def bg_space(self, p): return (
        p[0] + self.camera_space.x,
        p[1] + self.camera_space.y,
    )

    def update(self, scroll_vec):
        self.camera_space.move(
            scroll_vec[0] * self.speed,
            scroll_vec[1] * self.speed,
        )
        self.camera_space.clamp(self.bg.rect)
