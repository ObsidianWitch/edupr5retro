import shared.retro as retro
from shared.directions import Directions

class Camera:
    def __init__(self, window, bg, position):
        self.window = window
        self.bg = bg

        self.camera_space = window.rect().move(position)

        offset = 20
        self.scroll_zone_up = retro.Rect(0, 0, window.rect().w, offset)

        self.scroll_zone_down = self.scroll_zone_up.copy()
        self.scroll_zone_down.bottomleft = (0, window.rect().h)

        self.scroll_zone_left = retro.Rect(0, 0, offset, window.rect().h)

        self.scroll_zone_right = self.scroll_zone_left.copy()
        self.scroll_zone_right.topright = (window.rect().w, 0)

        self.speed = 10

    def scroll_vec(self, p): return Directions(
        up    = self.scroll_zone_up.collidepoint(p),
        down  = self.scroll_zone_down.collidepoint(p),
        left  = self.scroll_zone_left.collidepoint(p),
        right = self.scroll_zone_right.collidepoint(p),
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
