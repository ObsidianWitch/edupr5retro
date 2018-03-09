import pygame
class Clock:
    def __init__(self, framerate):
        self.clock = pygame.time.Clock()
        self.framerate = framerate

    @classmethod
    def time(cls): return pygame.time.get_ticks()

    def tick(self): return self.clock.tick(self.framerate)
