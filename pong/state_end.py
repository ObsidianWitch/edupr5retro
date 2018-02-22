import pygame

class StateEnd:
    def __init__(self, window, winner):
        self.window  = window
        self.winner  = winner
        self.restart = False

    def run(self):
        # Update
        self.restart = self.window.keys[pygame.K_SPACE]

        # Draw
        win_surface = self.window.fonts[4].render(
            f"JOUEUR {self.winner} GAGNANT", # text
            False,                           # antialias
            pygame.Color("yellow"),          # color
            pygame.Color("red")              # background color
        )
        self.window.screen.blit(
            win_surface,
            win_surface.get_rect(center = self.window.rect.center)
        )
