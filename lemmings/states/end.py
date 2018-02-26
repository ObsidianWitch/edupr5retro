import pygame

class End:
    def __init__(self, window, win):
        self.window = window
        self.restart = False
        self.txt_surface = self.window.fonts[4].render(
            "WIN" if win else "LOST", # text
            False,                    # antialias
            pygame.Color("white"),    # color
            pygame.Color("black"),    # background color
        )

    def run(self):
        # Update
        self.restart = self.window.keys[pygame.K_SPACE]

        # Draw
        self.window.screen.blit(
            self.txt_surface,
            self.txt_surface.get_rect(center = self.window.rect.center)
        )
