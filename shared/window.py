import sys
import pygame

class Window:
    def __init__(self, width, height, title, cursor = False):
        pygame.init()

        self.width  = width
        self.height = height
        self.screen = pygame.display.set_mode([self.width, self.height])

        pygame.display.set_caption(title)
        pygame.mouse.set_visible(cursor)

        self.clock = pygame.time.Clock()

        self.events = []

    def loop(self, instructions):
        while 1:
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT: sys.exit()

            instructions()

            self.clock.tick(30) # 30 FPS

            pygame.display.flip() # update display Surface
