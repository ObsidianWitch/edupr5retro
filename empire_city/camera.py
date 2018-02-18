import pygame

from shared.math import Directions

class Camera:
    def __init__(self, window, bg, position):
        self.window = window
        self.bg = bg

        self.display_zone = window.rect.move(position)

        offset = 100
        self.scroll_zone_up = pygame.Rect(0, 0, window.width, offset)

        self.scroll_zone_down = self.scroll_zone_up.copy()
        self.scroll_zone_down.bottomleft = (0, window.height)

        self.scroll_zone_left = pygame.Rect(0, 0, offset, window.height)

        self.scroll_zone_right = self.scroll_zone_left.copy()
        self.scroll_zone_right.topright = (window.width, 0)

        self.speed = 10

    def scroll_zone_collide(self, p): return Directions(
        up    = self.scroll_zone_up.collidepoint(p),
        down  = self.scroll_zone_down.collidepoint(p),
        left  = self.scroll_zone_left.collidepoint(p),
        right = self.scroll_zone_right.collidepoint(p),
    )

    def update(self, scroll_vec):
        self.display_zone.move_ip(
            scroll_vec[0] * self.speed,
            scroll_vec[1] * self.speed,
        )
        self.display_zone.clamp_ip(self.bg.rect)
