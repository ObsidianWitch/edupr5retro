import pygame

class StateEnd:
    def __init__(self, window):
        self.window  = window
        self.restart = False

    def run(self):
        # Update
        self.restart = self.window.keydown(pygame.K_SPACE)

        # Draw
        end_surface = self.window.fonts[4].render(
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
