import pygame

class StateEnd:
    def __init__(self, window):
        self.window = window

        self.font = pygame.font.SysFont("arial", 42)

    def run(self):
        # Update
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]: return True

        # Draw
        win_surface = self.font.render(
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
