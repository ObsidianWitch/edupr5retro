import collections

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

player = Player(window)
maze = Maze(window)

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

def game():
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

    # Draw
    maze.draw()
    player.draw()

window.loop(game)
