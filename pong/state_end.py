import pygame

class StateEnd:
    def __init__(self, window, winner):
        self.window = window
        self.winner = winner

    def run(self):
        # Update
        if self.window.keys[pygame.K_SPACE]: return True

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

        return False
