import pygame

class StateEnd:
    def __init__(self, window):
        self.window  = window
        self.restart = False

    def run(self):
        # Update
        self.restart = self.window.keys[pygame.K_SPACE]

        # Draw
        win_surface = self.window.fonts[4].render(
            "WIN",                 # text
            False,                 # antialias
            pygame.Color("white"), # color
            pygame.Color("black"), # background color
        )
        self.window.screen.blit(
            win_surface,
            win_surface.get_rect(center = self.window.rect.center)
        )

        return False
