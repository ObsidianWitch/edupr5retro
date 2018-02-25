import pygame

class Ball:
    def __init__(self, window):
        self.window = window

        self.x = 50
        self.y = self.window.height // 2

        self.dx = 3
        self.dy = 3

        self.radius = 10

        self.toggle = False
        self.inner_color = (
            pygame.Color("red"),
            pygame.Color("green")
        )

    @property
    def position(self): return (self.x, self.y)

    @property
    def speed(self): return (self.dx, self.dy)

    def bounce(self, dx_mul = 1, dy_mul = 1):
        y_collision = (self.y > self.window.height or self.y < 0)
        x_collision = (self.x > self.window.width or self.x < 0)

        if (not y_collision) and (not x_collision): return

        if y_collision: self.dy *= -1
        if x_collision: self.dx *= -1

        self.toggle = not self.toggle

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.bounce()

    def draw(self):
        pygame.draw.circle(
            self.window.screen,   # surface
            pygame.Color("blue"), # color
            self.position,        # position
            self.radius * 2,      # radius
        )
        pygame.draw.circle(
            self.window.screen,            # surface
            self.inner_color[self.toggle], # color
            self.position,                 # position
            self.radius,                   # radius
        )
