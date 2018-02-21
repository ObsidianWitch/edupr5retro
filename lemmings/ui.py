import pygame

from shared.sprite import Sprite
from lemmings.common import asset_path
from lemmings.lemming import STATES

class UI:
    def __init__(self, window):
        self.window = window

        self.group = pygame.sprite.Group()
        self.populate_sprites()
        self.position_sprites()

    def populate_sprites(self):
        stop_sprite = Sprite.from_path(asset_path("ui_stop.png"))
        stop_sprite.state = STATES.STOP
        self.group.add(stop_sprite)
        self.selection = stop_sprite

        # DEBUG
        test_sprite = Sprite.from_path(asset_path("ui_stop.png"))
        test_sprite.state = STATES.STOP
        self.group.add(test_sprite)

    def position_sprites(self):
        rect = pygame.Rect(
            0, 0,
            len(self.group) * self.selection.rect.width,
            self.selection.rect.height
        )
        rect.midbottom = self.window.rect.midbottom

        for i, s in enumerate(self.group):
            s.rect.top  = rect.top
            s.rect.left = rect.left + (i * s.rect.width)

    def update(self):
        if not self.window.mousedown(): return

        pos = pygame.mouse.get_pos()
        for s in self.group:
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
        self.group.draw(self.window.screen)
        self.draw_selection()
