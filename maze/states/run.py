import shared.retro as retro
import shared.collisions
from shared.directions import Directions
from shared.sprite import Sprite
from maze.nodes.maze import Maze
from maze.nodes.player import Player
from maze.nodes.palette import *

class StateRun:
    def __init__(self, window):
        self.window = window
        self.player = Player(window)
        self.maze = Maze(window)
        self.win = False

    def draw_score(self):
        score = Sprite(self.window.fonts[0].render(
            text  = f"Score: {self.player.score}",
            color = retro.WHITE,
        ))
        score.rect.topright = self.window.rect().topright
        score.rect.move(-10, 10)
        score.draw(self.window)

    def run(self):
        # Update
        key = self.window.events.key_hold
        self.player.update(
            directions = Directions(
                up    = key(retro.K_UP),
                down  = key(retro.K_DOWN),
                left  = key(retro.K_LEFT),
                right = key(retro.K_RIGHT),
            ),
            collisions = shared.collisions.pixel_vertices(
                surface = self.window,
                rect    = self.player.rect,
                color   = MAZE_PALETTE["B"],
            ),
        )

        ## Traps
        if shared.collisions.sprites(
            sprite = self.player,
            lst    = self.maze.traps,
            kill   = False,
        ): self.player.reset_position()

        ## Treasures
        if shared.collisions.sprites(
            sprite = self.player,
            lst    = self.maze.treasures,
            kill   = True
        ): self.player.score += 100

        ## Exit
        self.win = shared.collisions.distance(
            p1 = self.player.rect.center,
            p2 = self.maze.exit.rect.center,
            threshold = 5
        )

        # Draw
        self.maze.draw()
        self.player.draw()
        self.draw_score()
