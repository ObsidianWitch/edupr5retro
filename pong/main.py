import pygame

from pong.ball import Ball
from pong.paddle import *
from shared.window import Window

window = Window(
    width  = 600,
    height = 400,
    title  = "Pong"
)

def text_centerpos(font, text):
    return (
        window.width  // 2 - font.size(text)[0] // 2,
        window.height // 2 - font.size(text)[1] // 2
    )
font1 = pygame.font.SysFont("arial", 24)
font2 = pygame.font.SysFont("arial", 42)

pygame.mouse.set_visible(0) # hide cursor

paddle1 = Paddle(
    window   = window,
    position = Position.LEFT
)
paddle2 = Paddle(
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
    paddle1.update(keys)
    paddle2.update(keys)
    ball.update()

    ## ball x paddles collisions
    def ball_paddle1_collision():
        if (ball.x - ball.radius < paddle1.x + paddle1.width):
            if (ball.y >= paddle1.y) and (ball.y <= paddle1.y + paddle1.height):
                ball.x = paddle1.x + paddle1.width + ball.radius
                ball.dx *= -1
            else: ball.outside_reach = True

    def ball_paddle2_collision():
        if (ball.x + ball.radius > paddle2.x):
            if (ball.y >= paddle2.y) and (ball.y <= paddle2.y + paddle2.height):
                ball.x = paddle2.x - ball.radius
                ball.dx *= -1
            else: ball.outside_reach = True

    ## Make sure the ball does not bounce once it is beyond the reach of
    ## a paddle.
    if not ball.outside_reach:
        ball_paddle1_collision()
        ball_paddle2_collision()

    ## Edges collision
    if (ball.x + 2*ball.radius < 0):
        paddle2.score += 1
        ball.reset()
    if (ball.x - 2*ball.radius > window.width):
        paddle1.score += 1
        ball.reset()

    ## State
    if   paddle1.score == 3: state = State.P1WIN
    elif paddle2.score == 3: state = State.P2WIN

    # Draw
    window.screen.fill(pygame.Color("black"))
    paddle1.draw()
    paddle2.draw()
    ball.draw()

    score_text = f"{paddle1.score} - {paddle2.score}"
    score_surface = font1.render(
        score_text,           # text
        True,                 # antialias
        pygame.Color("green") # color
    )
    window.screen.blit(
        score_surface,
        (text_centerpos(font1, score_text)[0], 10)
    )

def state_end():
    win_text = f"JOUEUR {state.value - 1} GAGNANT"
    win_surface = font2.render(
        win_text,               # text
        True,                   # antialias
        pygame.Color("yellow"), # color
        pygame.Color("red")     # background color
    )
    window.screen.blit(
        win_surface,
        text_centerpos(font2, win_text)
    )

window.loop(game)
