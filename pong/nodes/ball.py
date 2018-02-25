import pygame

class Ball:
    def __init__(self, window):
        self.window = window
        self.radius = 10
        self.reset()

    @property
    def position(self): return (self.x, self.y)

    def reset(self):
        self.x  = self.window.width // 2
        self.y  = self.window.height // 2
        self.dx = -2
        self.dy = -2

    def walls_collision(self):
        if (self.y - self.radius < 0):
            self.y = self.radius
            self.dy *= -1
        if (self.y + self.radius > self.window.height):
            self.y = self.window.height - self.radius
            self.dy *= -1

    # Return -1 for left edge collision, 1 for right edge collision
    # and 0 otherwise.
    def edges_collision(self):
        left_edge  = (self.x + 2 * self.radius < 0)
        right_edge = (self.x - 2 * self.radius > self.window.width)

        if left_edge or right_edge: self.reset()

        return right_edge - left_edge

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.walls_collision()

    def draw(self):
        pygame.draw.circle(
            self.window.screen,    # surface
            pygame.Color("white"), # color
            self.position,         # position
            self.radius            # radius
        )
