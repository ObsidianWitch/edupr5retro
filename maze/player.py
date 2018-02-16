import pygame
import numpy

from shared.sprite import Sprite
from maze.palette import palette

class Player:
    char0_ascii = [
        '   RRR    ',
        '  RRWWR   ',
        '   RRR    ',
        '   YY     ',
        '   YYY    ',
        '   YY YG  ',
        '   GG     ',
        '   CC     ',
        '   CC     ',
        '  C  C    ',
        ' C    C   ',
    ]

    char1_ascii = [
        '   RRR    ',
        '  RRWWR   ',
        '   RRR    ',
        '   YY     ',
        '   YYY    ',
        '   YY YG  ',
        '   GG     ',
        '   CC     ',
        '   CC     ',
        '  C  C    ',
        '  C  C    ',
    ]

    char2_ascii = [
        '   RRR    ',
        '  RRWWR   ',
        '   RRR    ',
        '   YY     ',
        '   YYY    ',
        '   YY YG  ',
        '   GG     ',
        '   CC     ',
        '   CC     ',
        '   CC     ',
        '   CC     ',
    ]

    char3_ascii = [
        '    RRR   ',
        '   RWWRR  ',
        '    RRR   ',
        '     YY   ',
        '    YYY   ',
        '  GY YY   ',
        '     GG   ',
        '     CC   ',
        '     CC   ',
        '    C  C  ',
        '   C    C ',
    ]

    char4_ascii = [
        '    RRR   ',
        '   RWWRR  ',
        '    RRR   ',
        '     YY   ',
        '    YYY   ',
        '  GY YY   ',
        '     GG   ',
        '     CC   ',
        '     CC   ',
        '    C  C  ',
        '    C  C  ',
    ]

    char5_ascii = [
        '    RRR   ',
        '   RWWRR  ',
        '    RRR   ',
        '     YY   ',
        '    YYY   ',
        '  GY YY   ',
        '     GG   ',
        '     CC   ',
        '     CC   ',
        '     CC   ',
        '     CC   ',
    ]

    def __init__(self, window):
        self.window = window

        # keep track of the current direction the player is facing
        self.dir_x = 1

        self.sprite = Sprite.from_ascii_sprites(
            ascii_sprites = [
                self.char0_ascii,
                self.char1_ascii,
                self.char2_ascii,
                self.char3_ascii,
                self.char4_ascii,
                self.char5_ascii,
            ],
            animations = {
                "IDLE_R": [1],
                "IDLE_L": [4],
                "WALK_R": [0, 1, 2, 1],
                "WALK_L": [3, 4, 5, 4],
            },
            dictionary = palette,
            position   = (25, 25),
            colorkey   = palette[' '],
        )

    def move(self, keys):
        move_dir = (
            keys[pygame.K_RIGHT] - keys[pygame.K_LEFT],
            keys[pygame.K_DOWN]  - keys[pygame.K_UP]
        )
        self.sprite.rect.move_ip(move_dir[0], move_dir[1])

        walking = any(d != 0 for d in move_dir)
        if move_dir[0] != 0: self.dir_x = move_dir[0]
        self.animate(walking)

    def animate(self, walking):
        if not walking:
            if   self.dir_x < 0: self.sprite.animation = "IDLE_L"
            elif self.dir_x > 0: self.sprite.animation = "IDLE_R"
        else:
            if   self.dir_x < 0: self.sprite.animation = "WALK_L"
            elif self.dir_x > 0: self.sprite.animation = "WALK_R"

    def update(self, keys):
        self.move(keys)
        self.sprite.update()

    def draw(self):
        self.window.screen.blit(self.sprite.image, self.sprite.rect.topleft)
