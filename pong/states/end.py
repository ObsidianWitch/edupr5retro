import pygame

class StateEnd:
    def __init__(self, window, winner):
        self.window = window
        self.restart = False
        self.txt_surface = self.window.fonts[4].render(
            f"JOUEUR {winner} GAGNANT", # text
            False,                           # antialias
            pygame.Color("yellow"),          # color
            pygame.Color("red")              # background color
        )

    def run(self):
        # Update
        self.restart = self.window.keys[pygame.K_SPACE]

        # Draw
        self.window.screen.blit(
            self.txt_surface,
            self.txt_surface.get_rect(center = self.window.rect.center)
        )
