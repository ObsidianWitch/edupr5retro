import pygame

class StateEnd:
    def __init__(self, window):
        self.window = window

        self.font = pygame.font.SysFont("arial", 42)

    def run(self):
        # Update
        if self.window.keydown(pygame.K_SPACE): return True

        # Draw
        end_surface = self.font.render(
            "DEAD",                # text
            False,                 # antialias
            pygame.Color("white"), # color
            pygame.Color("black"), # background color
        )
        self.window.screen.blit(
            end_surface,
            end_surface.get_rect(center = self.window.rect.center)
        )

        return False
