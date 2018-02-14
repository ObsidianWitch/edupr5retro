import pygame

class Ball:
    def __init__(self, window):
        self.window = window

        self.reset()

        self.dx = -2
        self.dy = -2

        self.radius = 10

    def reset(self):
        self.x = self.window.width // 2
        self.y = self.window.height // 2

    def walls_collision(self):
        if (self.y - self.radius < 0):
            self.y = self.radius
            self.dy *= -1
        if (self.y + self.radius > self.window.height):
            self.y = self.window.height - self.radius
            self.dy *= -1

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.walls_collision()

    def draw(self):
        pygame.draw.circle(
            self.window.screen,    # surface
            pygame.Color("white"), # color
            (self.x, self.y),      # position
            self.radius            # radius
        )
