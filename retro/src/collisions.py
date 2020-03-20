from retro.src.directions import Directions

class Collisions:
    @classmethod
    def pixel_checker(cls, surface, color):
        def check(p, offset):
            p = (p[0] + offset[0], p[1] + offset[1])
            if not surface.rect().collidepoint(p):
                return None
            return (surface[p] == color)

        return check

    # Check collisions between `rect` midpoints and adjacent pixels of the
    # specified `color` in `surface`. For each direction, returns True on
    # collision, False on non-collisions, and None in case of undefined
    # behaviour (e.g. outside of the `surface` rect).
    @classmethod
    def pixel_mid(cls, surface, rect, color):
        check = cls.pixel_checker(surface, color)

        return Directions(
            up    = check(rect.midtop,    ( 0, -1)),
            down  = check(rect.midbottom, ( 0,  0)),
            left  = check(rect.midleft,   (-1,  0)),
            right = check(rect.midright,  ( 0,  0)),
        )

    # Check collision between `rect`'s topleft, topright, bottomleft,
    # bottomright points and adjacent pixels of the specified `color` in
    # `surface`. For each direction, returns True on collision, False on
    # non-collisions, and None in case of undefined behaviour (e.g. outside of
    # the `surface` rect).
    @classmethod
    def pixel_vertices(cls, surface, rect, color):
        check = cls.pixel_checker(surface, color)

        return Directions(
            up    = check(rect.topleft,     ( 0, -1))
                 or check(rect.topright,    (-1, -1)),
            down  = check(rect.bottomleft,  ( 0,  0))
                 or check(rect.bottomright, (-1,  0)),
            left  = check(rect.topleft,     (-1,  0))
                 or check(rect.bottomleft,  (-1, -1)),
            right = check(rect.topright,    ( 0,  0))
                 or check(rect.bottomright, ( 0, -1)),
        )

    # Returns a list containing all Sprites in `lst` that intersect with
    # `sprite`. If `kill` is set to True, all Sprites that collide will be
    # removed from `lst`.
    @classmethod
    def sprites(cls, sprite, lst, kill):
        collisions = []
        for s in lst:
            if sprite.rect.colliderect(s):
                collisions.append(s)
                if kill: s.kill()
        return collisions
