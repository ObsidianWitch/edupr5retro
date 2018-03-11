import include.retro as retro
import shared.collisions
from shared.sprite import Sprite
from pong.nodes.ball import Ball
from pong.nodes.paddle import Paddle

class StateRun:
    def __init__(self, window):
        self.window = window
        self.p1 = Paddle(self.window, Paddle.SIDE.LEFT)
        self.p2 = Paddle(self.window, Paddle.SIDE.RIGHT)
        self.ball = Ball(self.window)

    @property
    def winner(self):
        if   self.p1.score == 3: return 1
        elif self.p2.score == 3: return 2
        else: return 0

    def ball_paddle_collision(self, paddle):
        collision = shared.collisions.circle_rect(self.ball.circle, paddle.rect)
        if (collision == -1):
            self.ball.circle.left = paddle.rect.right
            self.ball.dx *= -1
        elif (collision == 1):
            self.ball.circle.right = paddle.rect.left
            self.ball.dx *= -1

    def draw_score(self):
        score = Sprite(self.window.fonts[1].render(
            text  = f"{self.p1.score} - {self.p2.score}",
            color = retro.GREEN,
        ))
        score.rect.midtop = self.window.rect.midtop
        score.rect.move(0, 10)
        score.draw(self.window)

    def run(self):
        # Update
        self.p1.update()
        self.p2.update()
        self.ball.update()

        self.ball_paddle_collision(self.p1)
        self.ball_paddle_collision(self.p2)

        edge = self.ball.edges_collision()
        if   edge < 0: self.p2.score += 1
        elif edge > 0: self.p1.score += 1

        # Draw
        self.window.fill(retro.BLACK)
        self.p1.draw()
        self.p2.draw()
        self.ball.draw()
        self.draw_score()
