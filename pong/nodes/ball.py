import pygame

from shared.circle import Circle

class Ball:
    def __init__(self, window):
        self.window = window
        self.reset(-1)

    def reset(self, side):
        self.circle = Circle(
            center = [self.window.width // 2, self.window.height // 2],
            radius = 10,
        )
        self.dx =  2 * side
        self.dy = -2

    def walls_collision(self):
        if (self.circle.top < 0):
            self.circle.top = 0
            self.dy *= -1
        if (self.circle.bottom > self.window.height):
            self.circle.bottom = self.window.height
            self.dy *= -1

    # Return -1 for left edge collision, 1 for right edge collision
    # and 0 otherwise.
    def edges_collision(self):
        left_edge  = (self.circle.right < 0)
        right_edge = (self.circle.left > self.window.width)
        collision = (right_edge - left_edge)
        if (collision != 0): self.reset(collision)
        return collision

    def update(self):
        self.circle.x += self.dx
        self.circle.y += self.dy
        self.walls_collision()

    def draw(self):
        pygame.draw.circle(
            self.window.screen,    # surface
            pygame.Color("white"), # color
            self.circle.center,    # position
            self.circle.radius     # radius
        )
