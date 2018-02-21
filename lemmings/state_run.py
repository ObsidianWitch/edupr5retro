import pygame

from lemmings.common  import asset_path
from lemmings.lemmings import Lemmings

class StateRun:
    def __init__(self, window):
        self.window = window
        self.bg = pygame.image.load(asset_path("map.png"))
        self.lemmings = Lemmings(self.window, self.bg)

    def draw_cursor(self):
        display = next(
            (e.type == pygame.MOUSEBUTTONDOWN for e in self.window.events),
            False
        )
        if not display: return

        pos = pygame.mouse.get_pos()
        rect = pygame.Rect(0, 0, 3, 3)
        rect.center = pos
        pygame.draw.rect(
            self.window.screen,
            pygame.Color("white"),
            rect
        )
        print(f"Click - Grid coordinates: {pos}")

    def run(self):
        # update
        self.lemmings.generate()
        self.lemmings.update()

        # Draw
        self.window.screen.blit(self.bg, (0,0))
        self.draw_cursor()
        self.lemmings.draw()
