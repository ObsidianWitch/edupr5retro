import pygame
from src.rect import Rect

pygame.init()

def test1():
    r1 = Rect(0, 1, 2, 3)
    r2 = Rect((4, 5), (6, 7))
    r3 = Rect(pygame.Rect(8, 9, 10, 11))

    print(r1, r2, r3)

    assert len(r1) == 4
    assert r1[0] == 0
    r1[0] = 12
    assert r1[0] == 12

def test2():
    r1 = Rect(0, 1, 2, 3)
    r2 = Rect(0, 1, 2, 3)
    r3 = Rect(0, 1, 2, 4)

    assert r1 == r2
    assert r3 != r1

    r4 = r1.copy()
    assert isinstance(r1, Rect)
    assert isinstance(r4, Rect)

    r1.move(5, 5)
    assert r1 == Rect(5, 6, 2, 3)
    r1.move((5, 5))
    assert r1 == Rect(10, 11, 2, 3)

def test3():
    r1 = Rect(5, 5, 10, 10)
    r2 = Rect(0, 0, 5, 5)
    r3 = Rect(15, 0, 5, 5)
    r4 = Rect(0, 15, 5, 5)
    r5 = Rect(15, 15, 5, 5)

    r2.clamp(r1)
    r3.clamp(r1)
    r4.clamp(r1)
    r5.clamp(r1)

    assert r2 == Rect(5, 5, 5, 5)
    assert r3 == Rect(10, 5, 5, 5)
    assert r4 == Rect(5, 10, 5, 5)
    assert r5 == Rect(10, 10, 5, 5)

def test4():
    r1 = Rect(0, 0, 5, 5)
    r2 = Rect(4, 4, 5, 5)

    r3 = r1.union(r2)
    r4 = r1.intersection(r2)

    assert r3 == Rect(0, 0, 9, 9)
    assert r4 == Rect(4, 4, 1, 1)

def test5():
    r1 = Rect(0, 0, 5, 5)
    r2 = Rect(4, 4, 5, 5)
    r3 = Rect(5, 5, 2, 2)
    p1 = (2, 2)
    p2 = (6, 6)

    assert r1.collidepoint(p1)
    assert r1.collidepoint(2, 2)
    assert not r1.collidepoint(p2)
    assert r1.colliderect(r2)
    assert r2.contains(r3)

test1()
test2()
test3()
test4()
test5()
