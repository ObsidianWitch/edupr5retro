from src.vector import Vector

def v1():
    va = (2,)
    vb = (4,)

    assert Vector.eq(va, va)
    assert Vector.ne(va, vb)
    assert Vector.eq(
        Vector.add(va, vb),
        (6,)
    )
    assert Vector.eq(
        Vector.sub(va, vb),
        (-2,)
    )
    assert Vector.dot(va, vb) == 8

def v2():
    va = (2, 3)
    vb = (4, 5)

    assert Vector.eq(va, va)
    assert Vector.ne(va, vb)
    assert Vector.eq(
        Vector.add(va, vb),
        (6, 8)
    )
    assert Vector.eq(
        Vector.sub(va, vb),
        (-2, -2)
    )
    assert Vector.dot(va, vb) == 23

def v10():
    va = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    vb = va[::-1]

    assert Vector.eq(va, va)
    assert Vector.ne(va, vb)
    assert Vector.eq(
        Vector.add(va, vb),
        (11, 11, 11, 11, 11, 11, 11, 11, 11, 11)
    )
    assert Vector.eq(
        Vector.sub(va, vb),
        (-9, -7, -5, -3, -1, 1, 3, 5, 7, 9)
    )
    assert Vector.dot(va, vb) == 220

v1()
v2()
v10()
