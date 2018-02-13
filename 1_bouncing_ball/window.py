import sys
import pygame

class Window:
    def __init__(self, width, height, title):
        pygame.init()

        self.width  = width
        self.height = height
        self.screen = pygame.display.set_mode([self.width, self.height])

        pygame.display.set_caption(title)

        self.clock = pygame.time.Clock()

    def loop(self, instructions):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

            instructions()

            self.clock.tick(30) # 30 FPS

            pygame.display.flip() # update display Surface
