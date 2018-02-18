import math

import pygame

from shared.math  import Directions
from maze.palette import palette
from maze.maze    import Maze
from maze.player  import Player

class StateRun:
    def __init__(self, window):
        self.window = window

        self.player = Player(window)
        self.maze = Maze(window)

    # Check collision between `sprite.rect`'s topleft, topright, bottomleft,
    # bottomright points and adjacent pixels of the specified `color`.
    # Only checking collision against `sprite.rect` midpoints would have caused
    # missed collision detection in some cases (near the rect's vertices).
    # To avoid this problem, we check the state of adjacent pixels to the vertices
    # of the current edge (e.g. topleft + (1, 0) and bottomleft + (1, 0) for the
    # left edge)
    def pixel_collision(self, rect, color):
        def check(p, vec):
            return (self.window.screen.get_at((
                p[0] + vec[0],
                p[1] + vec[1]
            )) == color)

        return Directions(
            up    = check(rect.topleft,  (0, -1))
                 or check(rect.topright, (0, -1)),
            down  = check(rect.bottomleft,  (0, 1))
                 or check(rect.bottomright, (0, 1)),
            left  = check(rect.topleft,    (-1, 0))
                 or check(rect.bottomleft, (-1, 0)),
            right = check(rect.topright,    (1, 0))
                 or check(rect.bottomright, (1, 0)),
    )

    def distance_collision(self, p1, p2, threshold):
        return math.sqrt(
                math.pow(p2[0] - p1[0], 2)
              + math.pow(p2[1] - p1[1], 2)
        ) < threshold

    def draw_score(self):
        score_surface = self.window.fonts[0].render(
            f"Score: {self.player.score}", # text
            False,                         # antialias
            pygame.Color("white")          # color
        )
        self.window.screen.blit(
            score_surface,
            score_surface.get_rect(
                topright = self.window.rect.topright
            ).move(-10, 10)
        )

    def run(self):
        # Update
        self.player.update(
            directions = Directions(
                up    = self.window.keys[pygame.K_UP],
                down  = self.window.keys[pygame.K_DOWN],
                left  = self.window.keys[pygame.K_LEFT],
                right = self.window.keys[pygame.K_RIGHT],
            ),
            collisions = self.pixel_collision(
                rect  = self.player.sprite.rect,
                color = pygame.Color(*palette["B"])
            ),
        )

        ## Traps
        if pygame.sprite.spritecollide(
            self.player.sprite, # sprite
            self.maze.traps,    # group
            False               # dokill
        ): self.player.reset_position()

        ## Treasures
        if pygame.sprite.spritecollide(
            self.player.sprite,  # sprite
            self.maze.treasures, # group
            True                 # dokill
        ): self.player.score += 100

        ## Exit
        if self.distance_collision(
            p1 = self.player.sprite.rect.center,
            p2 = self.maze.exit.rect.center,
            threshold = 5
        ): return True

        # Draw
        self.maze.draw()
        self.player.draw()
        self.draw_score()

        return False
