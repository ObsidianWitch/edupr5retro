import pygame
import numpy

import shared.math
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

        self.facing_x = 1

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

    def reset_pos(self):
        self.sprite.rect.topleft = (25, 25)

    def move(self, directions, collisions):
        move_vec = directions.vec
        collision_vec = collisions.vec

        for i,_ in enumerate(move_vec):
            if move_vec[i] == 0: continue
            move_vec[i] -= collision_vec[i]
            move_vec[i] = shared.math.clamp(move_vec[i], -1, 1)

        self.sprite.rect.move_ip(move_vec)

        walking = any(d != 0 for d in move_vec)
        if move_vec[0] != 0: self.facing_x = move_vec[0]
        self.animate(walking)

    def animate(self, walking):
        if not walking:
            if   self.facing_x < 0: self.sprite.animation = "IDLE_L"
            elif self.facing_x > 0: self.sprite.animation = "IDLE_R"
        else:
            if   self.facing_x < 0: self.sprite.animation = "WALK_L"
            elif self.facing_x > 0: self.sprite.animation = "WALK_R"

    def update(self, directions, collisions):
        self.move(directions, collisions)
        self.sprite.update()

    def draw(self):
        self.window.screen.blit(self.sprite.image, self.sprite.rect.topleft)
