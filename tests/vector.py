from src.vector import Vec

def v1():
    va = (2,)
    vb = (4,)

    assert Vec.eq(va, va)
    assert Vec.ne(va, vb)

    assert Vec.eq(
        Vec.add(va, vb),
        (6,)
    )

    assert Vec.eq(
        Vec.sub(va, vb),
        (-2,)
    )

    assert Vec.eq(
        Vec.mul(va, vb),
        (8,)
    )

    assert Vec.dot(va, vb) == 8

def v2():
    va = (2, 3)
    vb = (4, 5)

    assert Vec.eq(va, va)
    assert Vec.ne(va, vb)

    assert Vec.eq(
        Vec.add(va, vb),
        (6, 8)
    )

    assert Vec.eq(
        Vec.sub(va, vb),
        (-2, -2)
    )

    assert Vec.eq(
        Vec.mul(va, vb),
        (8, 15),
    )

    assert Vec.dot(va, vb) == 23

def v10():
    va = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    vb = va[::-1]

    assert Vec.eq(va, va)
    assert Vec.ne(va, vb)

    assert Vec.eq(
        Vec.add(va, vb),
        (11, 11, 11, 11, 11, 11, 11, 11, 11, 11)
    )

    assert Vec.eq(
        Vec.sub(va, vb),
        (-9, -7, -5, -3, -1, 1, 3, 5, 7, 9)
    )

    assert Vec.eq(
        Vec.mul(va, vb),
        (10, 18, 24, 28, 30, 30, 28, 24, 18, 10)
    )

    assert Vec.dot(va, vb) == 220

def v10n():
    va = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    n = 3

    assert Vec.eq(
        Vec.add(va, n),
        (4, 5, 6, 7, 8, 9, 10, 11, 12, 13)
    )
    assert Vec.eq(
        Vec.add(va, n),
        Vec.add(n, va),
    )

    assert Vec.eq(
        Vec.sub(va, n),
        (-2, -1, 0, 1, 2, 3, 4, 5, 6, 7)
    )
    assert Vec.eq(
        Vec.sub(n, va),
        (2, 1, 0, -1, -2, -3, -4, -5, -6, -7)
    )

    assert Vec.eq(
        Vec.mul(va, n),
        (3, 6, 9, 12, 15, 18, 21, 24, 27, 30)
    )
    assert Vec.eq(
        Vec.mul(va, n),
        Vec.mul(n, va),
    )

    assert Vec.dot(va, n) == 165
    assert Vec.dot(va, n) == Vec.dot(n, va)

v1()
v2()
v10()
v10n()
