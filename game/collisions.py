class Collisions:
    @classmethod
    def pxchecker(cls, image, color):
        def inside(p): return image.rect().collidepoint(p)

        def check(p, offset):
            p = (p[0] + offset[0], p[1] + offset[1])
            if not inside(p): return None
            return (image[p] == color)

        return check

    @classmethod
    def px1(cls, image, dir, rect, color):
        check = cls.pxchecker(image, color)
        if   dir[0] == -1: return check(rect.midleft,   (-1,  0))
        elif dir[0] ==  1: return check(rect.midright,  ( 0,  0))
        elif dir[1] == -1: return check(rect.midtop,    ( 0, -1))
        elif dir[1] ==  1: return check(rect.midbottom, ( 0,  0))
        else: return False

    @classmethod
    def px3(cls, image, dir, rect, color):
        check = cls.pxchecker(image, color)
        if dir[0] == -1: return (
            check(rect.topleft,       (-1,  0))
            or check(rect.midleft,    (-1,  0))
            or check(rect.bottomleft, (-1, -1))
        )
        elif dir[0] == 1: return (
            check(rect.topright,       ( 0,  0))
            or check(rect.midright,    ( 0,  0))
            or check(rect.bottomright, ( 0, -1))
        )
        elif dir[1] == -1: return (
            check(rect.topleft,     ( 0, -1))
            or check(rect.midtop,   ( 0, -1))
            or check(rect.topright, (-1, -1))
        )
        elif dir[1] == 1: return (
            check(rect.bottomleft,     ( 0,  0))
            or check(rect.midbottom,   ( 0,  0))
            or check(rect.bottomright, (-1,  0))
        )
        else: return False
