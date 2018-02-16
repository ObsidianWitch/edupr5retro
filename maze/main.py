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

def game():
    # Check collision between `sprite.rect` midtop, midbottom, midleft, midright
    # points and adjacent `window.screen` pixels of the specified `color`.
    # Caveat: It only detects collisions at midpoints. Any other point along the edge
    # will be undetected.
    def pixel_collision(sprite, color):
        def check(rect, vec):
            return (window.screen.get_at((
                rect[0] + vec[0],
                rect[1] + vec[1]
            )) == color)

        return Collision(
            top    = check(sprite.rect.midtop, (0, -1)),
            bottom = check(sprite.rect.midbottom, (0, 1)),
            left   = check(sprite.rect.midleft, (-1, 0)),
            right  = check(sprite.rect.midright, (1, 0)),
        )

    walls_collision = pixel_collision(player.sprite, pygame.Color(*palette["B"]))

    # Update
    keys = pygame.key.get_pressed()
    player.update(keys, walls_collision)

    # Draw
    maze.draw()
    player.draw()

window.loop(game)
