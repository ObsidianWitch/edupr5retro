from __future__ import annotations
import typing as typ
import pygame

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

class Rect(pygame.Rect):
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

    topleft     = lefttop = xy = lt = property_tuple('l',  't')
    midleft     = leftcenter   = lc = property_tuple('l',  'cy')
    bottomleft  = leftbottom   = lb = property_tuple('l',  'b')
    midtop      = centertop    = ct = property_tuple('cx', 't')
    center                     = cc = property_tuple('cx', 'cy')
    midbottom   = centerbottom = cb = property_tuple('cx', 'b')
    topright    = righttop     = rt = property_tuple('r',  't')
    midright    = rightcenter  = rc = property_tuple('r',  'cy')
    bottomright = rightbottom  = rb = property_tuple('r',  'b')

    width  = property_eqn('w')
    height = property_eqn('h')

    size = wh = property_tuple('w', 'h')

    def collide(self, shape: typ.Any) -> bool:
        if isinstance(shape, Rect):
            return self.colliderect(shape)
        else:
            raise NotImplementedError

    def __contains__(self, shape: typ.Any) -> bool:
        if isinstance(shape, typ.Sequence):
            return self.collidepoint(shape)
        elif isinstance(shape, Rect):
            return self.contains(shape)
        else:
            raise NotImplementedError
