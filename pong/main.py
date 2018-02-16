import pygame

from pong.ball import Ball
from pong.paddle import *
from shared.window import Window

window = Window(
    width  = 600,
    height = 400,
    title  = "Pong"
)

font1 = pygame.font.SysFont("arial", 24)
font2 = pygame.font.SysFont("arial", 42)

p1 = Paddle(
    window   = window,
    position = Position.LEFT
)
p2 = Paddle(
    window   = window,
    position = Position.RIGHT
)
ball = Ball(window)

State = Enum("State", "RUNNING P1WIN P2WIN")
state = State.RUNNING

def game():
    if state == State.RUNNING: state_running()
    else: state_end()

def state_running():
    global state

    # Update
    keys = pygame.key.get_pressed()

    p1.update(keys)
    p2.update(keys)
    ball.update()

    def ball_paddle_collision(paddle):
        left_collision = (ball.x > paddle.x) \
                     and (ball.x - ball.radius <= paddle.x + paddle.width)
        right_collision = (ball.x < paddle.x) \
                      and (ball.x + ball.radius >= paddle.x)
        height_collision = (ball.y >= paddle.y) \
                       and (ball.y <= paddle.y + paddle.height)

        if left_collision and height_collision:
            ball.x = paddle.x + paddle.width + ball.radius
            ball.dx *= -1
        if right_collision and height_collision:
            ball.x = paddle.x - ball.radius
            ball.dx *= -1

    ball_paddle_collision(p1)
    ball_paddle_collision(p2)

    ## Edges collision
    if (ball.x + 2*ball.radius < 0):
        p2.score += 1
        ball.reset()
    if (ball.x - 2*ball.radius > window.width):
        p1.score += 1
        ball.reset()

    ## State
    if   p1.score == 3: state = State.P1WIN
    elif p2.score == 3: state = State.P2WIN

    # Draw
    window.screen.fill(pygame.Color("black"))
    p1.draw()
    p2.draw()
    ball.draw()

    score_surface = font1.render(
        f"{p1.score} - {p2.score}", # text
        True,                       # antialias
        pygame.Color("green")       # color
    )
    window.screen.blit(
        score_surface,
        score_surface.get_rect(center = window.screen.get_rect().midtop)
                     .move(0, 20)
    )

def state_end():
    win_surface = font2.render(
        f"JOUEUR {state.value - 1} GAGNANT", # text
        True,                                # antialias
        pygame.Color("yellow"),              # color
        pygame.Color("red")                  # background color
    )
    window.screen.blit(
        win_surface,
        win_surface.get_rect(center = window.screen.get_rect().center)
    )

window.loop(game)
