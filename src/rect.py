from __future__ import annotations
import typing as typ

# Returns a property to an equation which depends on and sets `attr`, and
# depends on `mod`. By default `mod` is a lambda returning 0, meaning that
# `property_eqn` acts as an alias for the `attr` attribute.
#
# Example:
# cx = property_eqn('x', lambda self: self.w // 2)
# self.cx         -> self.x + (self.w // 2)
# self.cx = value -> self.cx = value - (self.w // 2)
def property_eqn(
    attr: str, mod: typ.Callable = lambda self: 0
) -> property:
    def fget(self: typ.Any) -> typ.Any:
        return getattr(self, attr) + mod(self)
    def fset(self: typ.Any, value: typ.Any) -> None:
        setattr(self, attr, value - mod(self))
    return property(fget, fset)

# Returns a property to a tuple of attributes `attrs`.
def property_tuple(*attrs: str) -> property:
    def fget(self: typ.Any) -> typ.Tuple:
        return tuple(getattr(self, attr) for attr in attrs)
    def fset(self: typ.Any, value: typ.Tuple) -> None:
        for i, attr in enumerate(attrs):
            setattr(self, attr, value[i])
    return property(fget, fset)

class Rect:
    # a---b---+c   | a: lefttop     == lt == xy == (left, top) == (x, y)
    # |·······|·   | b: centertop   == ct == (centerx, top)
    # |·······|·   | c: righttop    == rt == (right, top)
    # d···e···|f   | d: leftcenter  == lc == (left, centery)
    # |·······|·   | e: center      == cc == (centerx, centery)
    # |·······|·   | f: rightcenter == rc == (right, centery)
    # +-------+·   | g: leftbottom  == lb == (left, bottom)
    # g···h····i   | h: leftcenter  == lc == (centerx, bottom)
    #              | i: rightbottom == rb == (right, bottom)
    #              | size == wh == (w, h)
    def __init__(self, x: int, y: int, w: int, h: int) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    left    = l  = property_eqn('x')
    right   = r  = property_eqn('x', lambda self: self.w)
    centerx = cx = property_eqn('x', lambda self: self.w // 2)
    top     = t  = property_eqn('y')
    bottom  = b  = property_eqn('y', lambda self: self.h)
    centery = cy = property_eqn('y', lambda self: self.h // 2)

    lefttop = xy = lt = property_tuple('l',  't')
    leftcenter   = lc = property_tuple('l',  'cy')
    leftbottom   = lb = property_tuple('l',  'b')
    centertop    = ct = property_tuple('cx', 't')
    center       = cc = property_tuple('cx', 'cy')
    centerbottom = cb = property_tuple('cx', 'b')
    righttop     = rt = property_tuple('r',  't')
    rightcenter  = rc = property_tuple('r',  'cy')
    rightbottom  = rb = property_tuple('r',  'b')

    width  = property_eqn('w')
    height = property_eqn('h')

    size = wh = property_tuple('w', 'h')

    def copy(self) -> Rect:
        return self.__class__(self.x, self.y, self.w, self.h)

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy

    # Moves `self` to the nearest corner of `other` if `self` isn't completely
    # inside `other`. If `self` is too large to fit inside `other`, center it
    # horizontally and/or vertically. Returns whether `self` has been
    # clamped/centered or not.
    def clamp(self, other: Rect) -> bool:
        clamped = ((self.x < other.x) or (other.r < self.r)
                or (self.y < other.y) or (other.b < self.b))

        if self.x < other.x and other.r < self.r:
            self.cx = other.cx
        elif self.x < other.x:
            self.x = other.x
        elif other.r < self.r:
            self.r = other.r

        if self.y < other.y and other.b < self.b:
            self.cy = other.cy
        elif self.y < other.y:
            self.y = other.y
        elif other.b < self.b:
            self.b = other.b

        return clamped

    def collide(self, shape: typ.Any) -> bool:
        if isinstance(shape, Rect):
            return not ((shape.r <= self.l) or (shape.l >= self.r)
                     or (shape.b <= self.t) or (shape.t >= self.b))
        else:
            raise NotImplementedError

    def __contains__(self, shape: typ.Any) -> bool:
        if isinstance(shape, typ.Sequence):
            return ((self.l <= shape[0] < self.r)
                and (self.t <= shape[1] < self.b))
        elif isinstance(shape, Rect):
            return ((self.l <= shape.l) and (shape.r <= self.r)
                and (self.t <= shape.t) and (shape.b <= self.b))
        else:
            raise NotImplementedError

    def __eq__(self, other: typ.Any) -> bool:
        if not isinstance(other, Rect):
            raise NotImplementedError
        return (self.x == other.x) \
           and (self.y == other.y) \
           and (self.w == other.w) \
           and (self.h == other.h)

    def __iter__(self) -> typ.Generator[int, None, None]:
        yield self.x
        yield self.y
        yield self.w
        yield self.h

    def __repr__(self) -> str:
        return f'<rect({self.x}, {self.y}, {self.w}, {self.h})>'
