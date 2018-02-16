import pygame

class StateEnd:
    def __init__(self, window, winner):
        self.window = window
        self.font = pygame.font.SysFont(None, 42)

        self.winner = winner

    def run(self):
        # Update
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]: return True

        # Draw
        win_surface = self.font.render(
            f"JOUEUR {self.winner} GAGNANT", # text
            False,                           # antialias
            pygame.Color("yellow"),          # color
            pygame.Color("red")              # background color
        )
        self.window.screen.blit(
            win_surface,
            win_surface.get_rect(center = self.window.screen.get_rect().center)
        )

        return False
