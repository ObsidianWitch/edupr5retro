import pygame

import shared.collisions
from shared.directions  import Directions
from maze.nodes.maze import Maze
from maze.nodes.player import Player
from maze.nodes.palette import PALETTE

class StateRun:
    def __init__(self, window):
        self.window = window
        self.player = Player(window)
        self.maze = Maze(window)
        self.win = False

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
            collisions = shared.collisions.pixel_vertices(
                surface = self.window.screen,
                rect    = self.player.rect,
                color   = pygame.Color(*PALETTE["B"]),
            ),
        )

        ## Traps
        if pygame.sprite.spritecollide(
            self.player,     # sprite
            self.maze.traps, # group
            False            # dokill
        ): self.player.reset_position()

        ## Treasures
        if pygame.sprite.spritecollide(
            self.player,         # sprite
            self.maze.treasures, # group
            True                 # dokill
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
