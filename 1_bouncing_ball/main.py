import pygame

from ball import Ball
from window import Window

window = Window(
    width  = 800,
    height = 600,
    title  = "Bouncing Ball !!!"
)

ball = Ball(window)

def game_update():
    # Update
    ball.update()

    # Draw
    window.screen.fill(pygame.Color("white"))
    pygame.draw.rect(
        window.screen,                       # surface
        pygame.Color("green"),               # color
        [0, 0, window.width, window.height], # rect
        5                                    # width
    )
    ball.draw()

    # Debug
    print(f"position: ({ball.x}, {ball.y})\tspeed: ({ball.dx}, {ball.dy})")

window.loop(game_update)
