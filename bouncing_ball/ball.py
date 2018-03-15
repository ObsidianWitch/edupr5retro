import include.retro as retro
from shared.circle import Circle

class Ball:
    def __init__(self, window):
        self.window = window

        self.circle = Circle(
            center = [50, self.window.rect().h // 2],
            radius = 10,
        )
        self.dx = 3
        self.dy = 3

        self.toggle = False
        self.inner_color = (retro.RED, retro.GREEN)

    @property
    def speed(self): return (self.dx, self.dy)

    def bounce(self, dx_mul = 1, dy_mul = 1):
        y_collision = not (0 <= self.circle.y <= self.window.rect().h)
        x_collision = not (0 <= self.circle.x <= self.window.rect().w)

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
        self.window.draw_circle(
            color  = retro.BLUE,
            center = self.circle.center,
            radius = self.circle.radius * 2,
        )
        self.window.draw_circle(
            color  = self.inner_color[self.toggle],
            center = self.circle.center,
            radius = self.circle.radius,
        )
