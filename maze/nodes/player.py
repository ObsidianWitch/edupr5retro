import numpy
import shared.retro as retro
from maze.nodes.palette import *

class Player(retro.AnimatedSprite):
    PLAYER_ASCII = [
        ( # 0
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
        ),
        ( # 1
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
        ),
        ( # 2
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
        )
    ]
    PLAYER_ASCII += tuple( # flipped ascii frames (3, 4, 5)
        tuple(line[::-1] for line in frame_ascii)
        for frame_ascii in PLAYER_ASCII
    )

    def __init__(self, window):
        self.window = window

        self.facing_x = 1
        self.score = 0

        sprite = retro.AnimatedSprite.from_ascii(
            txts       = self.PLAYER_ASCII,
            dictionary = SPRITE_PALETTE,
            animations = retro.Animations(
                period  = 500,
                IDLE_R = [1],
                IDLE_L = [4],
                WALK_R = [0, 1, 2, 1],
                WALK_L = [3, 4, 5, 4],
            ),
        )
        retro.AnimatedSprite.__init__(self, sprite.images, sprite.animations)
        self.image.colorkey(SPRITE_PALETTE[' '])
        self.reset_position()

    def reset_position(self):
        self.rect.topleft = (25, 25)

    def move(self, directions, collisions):
        move_vec = directions.vec
        collision_vec = collisions.vec

        for i,_ in enumerate(move_vec):
            if move_vec[i] == 0: continue
            move_vec[i] -= collision_vec[i]
            move_vec[i] = retro.Math.clamp(move_vec[i], -1, 1)

        self.rect.move_ip(move_vec)

        if move_vec[0] != 0: self.facing_x = move_vec[0]
        walking = any(d != 0 for d in move_vec)
        self.animate(walking)

    def animate(self, walking):
        if not walking:
            if   self.facing_x < 0: self.animations.set("IDLE_L")
            elif self.facing_x > 0: self.animations.set("IDLE_R")
        else:
            if   self.facing_x < 0: self.animations.set("WALK_L")
            elif self.facing_x > 0: self.animations.set("WALK_R")

    def update(self, directions, collisions):
        self.move(directions, collisions)
        retro.AnimatedSprite.update(self)

    def draw(self):
        retro.AnimatedSprite.draw(self, self.window)
