import math

from shared.directions import Directions

def pixel_checker(surface, color):
    def inside(p): return surface.get_rect().collidepoint(p)

    def check(p, offset):
        p = (p[0] + offset[0], p[1] + offset[1])
        if not inside(p): return None
        return (surface.get_at(p) == color)

    return check

# Check collisions between `rect` midpoints and adjacent pixels of the specified
# `color` in `surface`.
# For each direction, returns True on collision, False on non-collisions, and
# None in case of undefined behaviour (e.g. outside of the `surface` rect).
def pixel_mid(surface, rect, color):
    check = pixel_checker(surface, color)

    return Directions(
        up    = check(rect.midtop,    ( 0, -1)),
        down  = check(rect.midbottom, ( 0,  0)),
        left  = check(rect.midleft,   (-1,  0)),
        right = check(rect.midright,  ( 0,  0)),
    )

# Check collision between `rect`'s topleft, topright, bottomleft,
# bottomright points and adjacent pixels of the specified `color` in `surface`.
# For each direction, returns True on collision, False on non-collisions, and
# None in case of undefined behaviour (e.g. outside of the `surface` rect).
def pixel_vertices(surface, rect, color):
    check = pixel_checker(surface, color)

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

def distance(p1, p2, threshold):
    return math.sqrt(
            math.pow(p2[0] - p1[0], 2)
          + math.pow(p2[1] - p1[1], 2)
    ) < threshold
