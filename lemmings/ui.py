import pygame

from shared.sprite import Sprite
from lemmings.nodes.lemming import STATES
from lemmings.path import asset_path

class UI:
    def __init__(self, window):
        self.window = window

        self.icons = pygame.sprite.Group()
        self.populate_icons()
        self.position_icons()

    def populate_icons(self):
        stop_sprite = Sprite.from_path(asset_path("ui_stop.png"))
        stop_sprite.state = STATES.STOP
        self.icons.add(stop_sprite)
        self.selection = stop_sprite

        digv_sprite = Sprite.from_path(asset_path("ui_digv.png"))
        digv_sprite.state = STATES.DIGV
        self.icons.add(digv_sprite)

    def position_icons(self):
        rect = pygame.Rect(
            0, 0,
            len(self.icons) * self.selection.rect.width,
            self.selection.rect.height
        )
        rect.midbottom = self.window.rect.midbottom

        for i, s in enumerate(self.icons):
            s.rect.top  = rect.top
            s.rect.left = rect.left + (i * s.rect.width)

    def update(self):
        if not self.window.mousedown(): return

        pos = pygame.mouse.get_pos()
        for s in self.icons:
            if s.rect.collidepoint(pos):
                self.selection = s

    def draw_selection(self):
        pygame.draw.rect(
            self.window.screen,    # surface
            pygame.Color("white"), # color
            self.selection.rect,   # rect
            2                      # width
        )

    def draw(self):
        self.icons.draw(self.window.screen)
        self.draw_selection()
