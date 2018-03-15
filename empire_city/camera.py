import include.retro as retro
from shared.directions import Directions

class Camera:
    def __init__(self, window, bg, position):
        self.window = window
        self.bg = bg

        self.display_zone = window.rect().move(position)

        offset = 20
        self.scroll_zone_up = retro.Rect(0, 0, window.rect().w, offset)

        self.scroll_zone_down = self.scroll_zone_up.copy()
        self.scroll_zone_down.bottomleft = (0, window.rect().h)

        self.scroll_zone_left = retro.Rect(0, 0, offset, window.rect().h)

        self.scroll_zone_right = self.scroll_zone_left.copy()
        self.scroll_zone_right.topright = (window.rect().w, 0)

        self.speed = 10

    def scroll_zone_collide(self, p): return Directions(
        up    = self.scroll_zone_up.collidepoint(p),
        down  = self.scroll_zone_down.collidepoint(p),
        left  = self.scroll_zone_left.collidepoint(p),
        right = self.scroll_zone_right.collidepoint(p),
    )

    def bg_space(self, p): return (
        p[0] + self.display_zone.x,
        p[1] + self.display_zone.y,
    )

    def update(self, scroll_vec):
        self.display_zone.move(
            scroll_vec[0] * self.speed,
            scroll_vec[1] * self.speed,
        )
        self.display_zone.clamp(self.bg.rect)
