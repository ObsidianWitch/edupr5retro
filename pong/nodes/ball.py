import include.retro as retro
from pong.nodes.circle import Circle

class Ball:
    def __init__(self, window):
        self.window = window
        self.reset(-1)

    def reset(self, side):
        self.circle = Circle(
            center = [self.window.rect().w // 2, self.window.rect().h // 2],
            radius = 10,
        )
        self.dx =  2 * side
        self.dy = -2

    def walls_collision(self):
        if (self.circle.top < 0):
            self.circle.top = 0
            self.dy *= -1
        if (self.circle.bottom > self.window.rect().h):
            self.circle.bottom = self.window.rect().h
            self.dy *= -1

    # Return -1 for left edge collision, 1 for right edge collision
    # and 0 otherwise.
    def edges_collision(self):
        left_edge  = (self.circle.right < 0)
        right_edge = (self.circle.left > self.window.rect().w)
        collision = (right_edge - left_edge)
        if (collision != 0): self.reset(collision)
        return collision

    def update(self):
        self.circle.x += self.dx
        self.circle.y += self.dy
        self.walls_collision()

    def draw(self):
        self.window.draw_circle(
            color  = retro.WHITE,
            center = self.circle.center,
            radius = self.circle.radius,
        )
