import pygame

from shared.window import Window
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

def game():
    # Update
    keys = pygame.key.get_pressed()
    player.update(keys)

    # Draw
    maze.draw()
    player.draw()

window.loop(game)
