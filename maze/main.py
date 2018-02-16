import collections

import pygame

from shared.window import Window
from maze.palette  import palette
from maze.maze     import Maze
from maze.player   import Player

Collision = collections.namedtuple("Collision", ["top", "bottom", "right", "left"])

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
# To avoid this problem, a pair of `sprite.rect` vertices are checked against
# two adjacent pixels.
def pixel_collision(sprite, color):
    def check(rect, vec):
        return (window.screen.get_at((
            rect[0] + vec[0],
            rect[1] + vec[1]
        )) == color)

    return Collision(
        top    = check(sprite.rect.topleft,  (0, -1))
              or check(sprite.rect.topright, (0, -1)),
        bottom = check(sprite.rect.bottomleft,  (0, 1))
              or check(sprite.rect.bottomright, (0, 1)),
        left   = check(sprite.rect.topleft,    (-1, 0))
              or check(sprite.rect.bottomleft, (-1, 0)),
        right  = check(sprite.rect.topright,    (1, 0))
              or check(sprite.rect.bottomright, (1, 0)),
    )

def game():
    walls_collision = pixel_collision(
        player.sprite,
        pygame.Color(*palette["B"])
    )

    # Update
    keys = pygame.key.get_pressed()
    player.update(keys, walls_collision)

    # Draw
    maze.draw()
    player.draw()

window.loop(game)
