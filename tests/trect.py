import itertools
import random
from pygame import Rect as PygRect
from src.rect import Rect as RetroRect

def test_properties():
    def helper_assert(r0, r1):
        assert r0.x == r1.x == r1.left == r1.l
        assert r0.right == r1.right == r1.r
        assert r0.centerx == r1.centerx == r1.cx
        assert r0.y == r1.y == r1.top == r1.t
        assert r0.bottom == r1.bottom == r1.b
        assert r0.centery == r1.centery == r1.cy

        assert r0.topleft == r1.lefttop == r1.xy == r1.lt
        assert r0.midleft == r1.leftcenter == r1.lc
        assert r0.bottomleft == r1.leftbottom == r1.lb
        assert r0.midtop == r1.centertop == r1.ct
        assert r0.center == r1.center == r1.cc
        assert r0.midbottom == r1.centerbottom == r1.cb
        assert r0.topright == r1.righttop == r1.rt
        assert r0.midright == r1.rightcenter == r1.rc
        assert r0.bottomright == r1.rightbottom == r1.rb

        assert r0.w == r1.w == r1.width
        assert r0.h == r1.h == r1.height

        assert r0.size == r1.size == r1.wh

    for x, y, w, h in itertools.product((-1, 0, 1), repeat = 4):
        x *= random.randrange(1, 1000000)
        y *= random.randrange(1, 1000000)
        w *= random.randrange(1, 1000000)
        h *= random.randrange(1, 1000000)

        r0 = PygRect(x, y, w, h)
        r1 = RetroRect(x, y, w, h)
        helper_assert(r0, r1)

        for attr in (
            'left', 'right', 'top', 'bottom',
            'centerx', 'centery', 'width', 'height'
        ):
            r0 = PygRect(x, y, w, h)
            r1 = RetroRect(x, y, w, h)
            rnd = random.randrange(1, 1000000)
            setattr(r0, attr, getattr(r0, attr) + rnd)
            setattr(r1, attr, getattr(r1, attr) + rnd)
            helper_assert(r0, r1)

def test_copy():
    r0 = RetroRect(0, 1, 2, 3)
    r1 = r0.copy()
    r2 = r0.copy()
    assert r0 == r1 == r2

    r0.x += 1
    assert r0 != r1
    assert r1 == r2

    r1.x += 2
    assert r0 != r1
    assert r1 != r2

def test_move():
    r0 = RetroRect(0, 1, 2, 3)
    r0.move(2, 3)
    assert r0.lt == (2, 4)

def test_clamp():
    other = RetroRect(0, 0, 8, 8)

    # self bigger horizontally & vertically
    self = RetroRect(-2, -2, 20, 20)
    assert self.clamp(other) == True
    assert self.cc == other.cc

    # self bigger vertically
    self = RetroRect(-2, -2, 4, 20)
    assert self.clamp(other) == True
    assert self.lc == other.lc

    # self bigger horizontally
    self = RetroRect(-2, -2, 20, 4)
    assert self.clamp(other) == True
    assert self.ct == other.ct

    # self lt corner outside
    self = RetroRect(-4, -4, 4, 4)
    assert self.clamp(other) == True
    assert self.lt == other.lt

    # self rt corner outside
    self = RetroRect(8, -4, 4, 4)
    assert self.clamp(other) == True
    assert self.rt == other.rt

    # self lb corner outside
    self = RetroRect(-4, 8, 4, 4)
    assert self.clamp(other) == True
    assert self.lb == other.lb

    # self rb corner outside
    self = RetroRect(8, 8, 4, 4)
    assert self.clamp(other) == True
    assert self.rb == other.rb

    # self intersect lt corner
    self = RetroRect(-2, -2, 4, 4)
    assert self.clamp(other) == True
    assert self.lt == other.lt

    # self inside lt corner
    self = RetroRect(0, 0, 4, 4)
    assert self.clamp(other) == False

    # self inside arbitrary
    self = RetroRect(1, 3, 4, 4)
    assert self.clamp(other) == False

def test_collide():
    self = RetroRect(0, 0, 8, 8)

    assert not RetroRect(-4, -4, 4, 4).collide(self)
    assert RetroRect(-2, -2, 4, 4).collide(self)
    assert RetroRect( 0,  0, 4, 4).collide(self)
    assert RetroRect( 4,  4, 4, 4).collide(self)
    assert RetroRect( 5,  5, 4, 4).collide(self)
    assert not RetroRect( 9,  9, 4, 4).collide(self)

def test_contains():
    self = RetroRect(0, 0, 8, 8)

    assert [-1, -1] not in self
    assert (-1,  0) not in self
    assert ( 0, -1) not in self
    assert ( 0,  0) in self
    assert ( 3,  5) in self
    assert ( 7,  7) in self
    assert ( 7,  8) not in self
    assert ( 8,  7) not in self
    assert ( 8,  8) not in self
    assert ( 9,  9) not in self

    assert RetroRect(-4, -4, 4, 4) not in self
    assert RetroRect(-2, -2, 4, 4) not in self
    assert RetroRect( 0,  0, 4, 4) in self
    assert RetroRect( 4,  4, 4, 4) in self
    assert RetroRect( 5,  5, 4, 4) not in self
    assert RetroRect( 9,  9, 4, 4) not in self

def test_eq():
    assert RetroRect(0, 0, 8, 8) == RetroRect(0, 0, 8, 8)
    assert RetroRect(0, 0, 8, 8) != RetroRect(1, 0, 8, 8)
    assert RetroRect(0, 0, 8, 8) != RetroRect(0, 1, 8, 8)
    assert RetroRect(0, 0, 8, 8) != RetroRect(0, 0, 9, 8)
    assert RetroRect(0, 0, 8, 8) != RetroRect(0, 0, 8, 9)

def test_iter():
    assert tuple(RetroRect(0, 1, 2, 3)) == (0, 1, 2, 3)

test_properties()
test_copy()
test_move()
test_clamp()
test_collide()
test_contains()
test_eq()
test_iter()
