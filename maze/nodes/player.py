import numpy
from retro.src import retro
from maze.path import asset

class Player(retro.Sprite):
    def __init__(self):
        self.facing_x = 1
        self.score = 0

        sprite = retro.Sprite.from_spritesheet(
            path = asset('player.png'),
            animations = retro.Animations(
                frame_size = (10, 11),
                period = 500,
                IDLE_R = ([1], 0),
                IDLE_L = ([4], 0),
                WALK_R = ([0, 1, 2, 1], 0),
                WALK_L = ([3, 4, 5, 4], 0),
            ),
        )
        retro.Sprite.__init__(self, sprite.image, sprite.animations)
        self.reset_position()

    def reset_position(self):
        self.rect.topleft = (25, 25)

    def move(self, directions, collisions):
        move_vec = directions.vec
        collision_vec = collisions.vec

        for i,_ in enumerate(move_vec):
            if move_vec[i] == 0: continue
            move_vec[i] -= collision_vec[i]
        move_vec = numpy.clip(move_vec, -1, 1)

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
