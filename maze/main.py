import math
import enum

import pygame

from shared.window import Window
from shared.math   import Directions
from maze.palette  import palette
from maze.maze     import Maze
from maze.player   import Player

window = Window(
    width  = 400,
    height = 400,
    title  = "Maze"
)

font = pygame.font.SysFont("arial", 42)

player = Player(window)
maze = Maze(window)

State = enum.Enum("State", "RUNNING END")
state = State.RUNNING

def game():
    if state == State.RUNNING: state_running()
    else: state_end()

# Check collision between `sprite.rect` topleft, topright, bottomleft,
# bottomright points and adjacent pixels of the specified `color`.
# Only checking collision against `sprite.rect` midpoints would have caused
# missed collision detection in some cases (near the rect's vertices).
# To avoid this problem, we check the state of adjacent pixels to the vertices
# of the current edge (e.g. topleft + (1, 0) and bottomleft + (1, 0) for the
# left edge)
def pixel_collision(sprite, color):
    def check(rect, vec):
        return (window.screen.get_at((
            rect[0] + vec[0],
            rect[1] + vec[1]
        )) == color)

    return Directions(
        up    = check(sprite.rect.topleft,  (0, -1))
             or check(sprite.rect.topright, (0, -1)),
        down  = check(sprite.rect.bottomleft,  (0, 1))
             or check(sprite.rect.bottomright, (0, 1)),
        left  = check(sprite.rect.topleft,    (-1, 0))
             or check(sprite.rect.bottomleft, (-1, 0)),
        right = check(sprite.rect.topright,    (1, 0))
             or check(sprite.rect.bottomright, (1, 0)),
    )

def distance_collision(p1, p2, threshold):
    return math.sqrt(
            math.pow(p2[0] - p1[0], 2)
          + math.pow(p2[1] - p1[1], 2)
    ) < threshold


def state_running():
    global state

    # Update
    keys = pygame.key.get_pressed()
    player.update(
        directions = Directions(
            up    = keys[pygame.K_UP],
            down  = keys[pygame.K_DOWN],
            left  = keys[pygame.K_LEFT],
            right = keys[pygame.K_RIGHT],
        ),
        collisions = pixel_collision(
            sprite = player.sprite,
            color  = pygame.Color(*palette["B"])
        ),
    )

    if distance_collision(
        p1 = player.sprite.rect.center,
        p2 = maze.exit.rect.center,
        threshold = 5
    ): state = State.END

    # Draw
    maze.draw()
    player.draw()

def state_end():
    win_surface = font.render(
        "WIN",                 # text
        True,                  # antialias
        pygame.Color("white"), # color
        pygame.Color("black"), # background color
    )

    window.screen.blit(
        win_surface,
        win_surface.get_rect(center = window.screen.get_rect().center)
    )

window.loop(game)
