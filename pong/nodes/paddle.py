import enum
import pygame

class Paddle:
    SIDE = enum.Enum("SIDE", "LEFT RIGHT")

    def __init__(self, window, side):
        self.window = window
        self.side = side
        self.rect = pygame.Rect(0, 0, 10, 50) # x, y, width, height

        offset = 20
        if side == self.SIDE.LEFT:
            self.rect.left = offset
        elif side == self.SIDE.RIGHT:
            self.rect.right = window.width - offset
        self.rect.centery = window.height // 2

        self.dy = 2
        self.score = 0

    def move(self, keys):
        if self.side == self.SIDE.LEFT:
            if keys[pygame.K_UP]:   self.rect.y -= self.dy
            if keys[pygame.K_DOWN]: self.rect.y += self.dy
        elif self.side == self.SIDE.RIGHT:
            if keys[pygame.K_a]: self.rect.y -= self.dy
            if keys[pygame.K_q]: self.rect.y += self.dy

    def walls_collision(self):
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.window.height:
            self.rect.bottom = self.window.height

    def update(self):
        self.move(self.window.keys)
        self.walls_collision()

    def draw(self):
        pygame.draw.rect(
            self.window.screen,    # surface
            pygame.Color("white"), # color
            self.rect,             # rect
        )
