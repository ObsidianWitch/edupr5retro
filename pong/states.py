from retro.src import retro
from pong.nodes.ball import Ball
from pong.nodes.paddle import Paddle

class Run:
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
        collision = self.ball.circle.collide(paddle.rect)
        if (collision == -1):
            self.ball.circle.left = paddle.rect.right
            self.ball.dx *= -1
        elif (collision == 1):
            self.ball.circle.right = paddle.rect.left
            self.ball.dx *= -1

    def draw_line(self):
        self.window.draw_line(
            start_pos = self.window.rect().midtop,
            end_pos   = self.window.rect().midbottom,
            color     = (200, 200, 200),
            width     = 2,
        )

    def draw_score(self):
        score = retro.Sprite(self.window.fonts[4].render(
            text  = f"{self.p1.score}   {self.p2.score}",
            color = (200, 200, 200),
        ))
        score.rect.midtop = self.window.rect().midtop
        score.rect.move_ip(0, 10)
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
        self.draw_line()
        self.p1.draw()
        self.p2.draw()
        self.ball.draw()
        self.draw_score()

class End:
    def __init__(self, window, winner):
        self.window = window
        self.restart = False

        self.txt = retro.Sprite(self.window.fonts[4].render(
            text    = f"P{winner} WINS",
            color   = retro.WHITE,
            bgcolor = retro.BLACK,
        ))
        self.txt.rect.center = self.window.rect().center

    def run(self):
        # Update
        key = self.window.events.key_press
        self.restart = key(retro.K_SPACE)

        # Draw
        self.txt.draw(self.window)
