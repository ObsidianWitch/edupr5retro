import pygame
from src.surface import Surface
from src.clock import Clock
class Window(Surface):
    def __init__(self, title, size, framerate = 30):
        pygame.init()
        pygame.mixer.quit()

        pygame.display.set_caption(title)
        self.pygsurface = pygame.display.set_mode(size)

        self.clock = Clock(framerate)

    def cursor(self, enable):
        pygame.mouse.set_visible(enable)

    def update(self):
        self.clock.tick()
        pygame.display.flip()
