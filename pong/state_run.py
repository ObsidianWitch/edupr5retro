import pygame

from pong.ball import Ball
from pong.paddle import *

class StateRun:
    def __init__(self, window):
        self.window = window
        self.font = pygame.font.SysFont(None, 24)

        self.p1 = Paddle(
            window   = self.window,
            position = Position.LEFT
        )
        self.p2 = Paddle(
            window   = self.window,
            position = Position.RIGHT
        )
        self.ball = Ball(self.window)

    def ball_paddle_collision(self, paddle):
        left_collision = (
                (self.ball.x > paddle.x)
            and (self.ball.x - self.ball.radius <= paddle.x + paddle.width)
        )
        right_collision = (
                (self.ball.x < paddle.x)
            and (self.ball.x + self.ball.radius >= paddle.x)
        )
        height_collision = (
                (self.ball.y >= paddle.y)
            and (self.ball.y <= paddle.y + paddle.height)
        )

        if left_collision and height_collision:
            self.ball.x = paddle.x + paddle.width + self.ball.radius
            self.ball.dx *= -1
        if right_collision and height_collision:
            self.ball.x = paddle.x - self.ball.radius
            self.ball.dx *= -1

    # Returns 0 while the game is not yet been won.
    # Returns which player won (1 or 2) when the game is finished.
    def run(self):
        # Update
        keys = pygame.key.get_pressed()

        self.p1.update(keys)
        self.p2.update(keys)
        self.ball.update()

        self.ball_paddle_collision(self.p1)
        self.ball_paddle_collision(self.p2)

        edge = self.ball.edges_collision()
        if   edge < 0: self.p2.score += 1
        elif edge > 0: self.p1.score += 1

        ## Win conditions
        if   self.p1.score == 3: return 1
        elif self.p2.score == 3: return 2

        # Draw
        self.window.screen.fill(pygame.Color("black"))
        self.p1.draw()
        self.p2.draw()
        self.ball.draw()

        score_surface = self.font.render(
            f"{self.p1.score} - {self.p2.score}", # text
            False,                      # antialias
            pygame.Color("green")       # color
        )
        self.window.screen.blit(
            score_surface,
            score_surface.get_rect(
                midtop = self.window.screen.get_rect().midtop
            ).move(0, 10)
        )

        return 0
