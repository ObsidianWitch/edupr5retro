import pygame

from bouncing_ball.ball import Ball
from shared.window import Window

window = Window(
    size  = (800, 600),
    title = "Bouncing Ball !!!",
)

ball = Ball(window)

def game():
    # Update
    ball.update()

    # Draw
    window.screen.fill(pygame.Color("white"))
    pygame.draw.rect(
        window.screen,         # surface
        pygame.Color("green"), # color
        window.rect,           # rect
        5                      # width
    )
    ball.draw()

    # Debug
    print(f"position: {ball.circle.center}\tspeed: {ball.speed}")

window.loop(game)
