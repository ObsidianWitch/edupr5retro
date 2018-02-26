import pygame

from shared.circle import Circle

class Ball:
    def __init__(self, window):
        self.window = window

        self.circle = Circle(
            center = [50, self.window.height // 2],
            radius = 10,
        )
        self.dx = 3
        self.dy = 3

        self.toggle = False
        self.inner_color = (
            pygame.Color("red"),
            pygame.Color("green")
        )

    @property
    def speed(self): return (self.dx, self.dy)

    def bounce(self, dx_mul = 1, dy_mul = 1):
        y_collision = not (0 <= self.circle.y <= self.window.height)
        x_collision = not (0 <= self.circle.x <= self.window.width)

        if y_collision:
            self.dy *= -1
            self.toggle = not self.toggle
        if x_collision:
            self.dx *= -1
            self.toggle = not self.toggle

    def update(self):
        self.circle.x += self.dx
        self.circle.y += self.dy
        self.bounce()

    def draw(self):
        pygame.draw.circle(
            self.window.screen,     # surface
            pygame.Color("blue"),   # color
            self.circle.center,     # position
            self.circle.radius * 2, # radius
        )
        pygame.draw.circle(
            self.window.screen,            # surface
            self.inner_color[self.toggle], # color
            self.circle.center,            # position
            self.circle.radius,            # radius
        )
