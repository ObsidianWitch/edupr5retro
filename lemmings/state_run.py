import pygame

from lemmings.common  import asset_path
from lemmings.lemmings import Lemmings

class StateRun:
    def __init__(self, window):
        self.window = window

        self.bg = pygame.image.load(asset_path("map.png"))
        self.lemmings = Lemmings(self.window)

    def draw_cursor(self):
        display = next(
            (e.type == pygame.MOUSEBUTTONDOWN for e in self.window.events),
            False
        )
        if not display: return

        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]
        pygame.draw.line(
            self.window.screen,
            pygame.Color("white"),
            (x - 5, y), (x + 5, y)
        )
        pygame.draw.line(
            self.window.screen,
            pygame.Color("white"),
            (x, y - 5), (x, y + 5)
        )
        print(f"Click - Grid coordinates: {x}, {y}")

    def run(self):
        # update
        self.lemmings.generate()
        self.lemmings.update()

        # Draw
        self.window.screen.blit(self.bg, (0,0))
        self.draw_cursor()
        self.lemmings.draw()
