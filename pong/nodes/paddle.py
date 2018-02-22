import enum
import pygame

class Paddle:
    SIDE = enum.Enum("SIDE", "LEFT RIGHT")

    def __init__(self, window, side):
        self.window = window

        self.width  = 10
        self.height = 50
        self.offset = 20

        self.side = side
        if side == self.SIDE.LEFT:
            self.x = self.offset
        elif side == self.SIDE.RIGHT:
            self.x = window.width - self.width - self.offset
        self.y = window.height // 2 - self.height // 2

        self.dy = 2

        self.score = 0

    def move(self, keys):
        if self.side == self.SIDE.LEFT:
            if keys[pygame.K_UP]:   self.y -= self.dy
            if keys[pygame.K_DOWN]: self.y += self.dy
        elif self.side == self.SIDE.RIGHT:
            if keys[pygame.K_a]: self.y -= self.dy
            if keys[pygame.K_q]: self.y += self.dy

    def walls_collision(self):
        if self.y - self.dy < 0:
            self.y = 0
        if self.y + self.height + self.dy > self.window.height:
            self.y = self.window.height - self.height

    def update(self, keys):
        self.move(keys)
        self.walls_collision()

    def draw(self):
        pygame.draw.rect(
            self.window.screen,                       # surface
            pygame.Color("white"),                    # color
            (self.x, self.y, self.width, self.height) # rect
        )
