from numbers import Number

class Vec:
    @classmethod
    def add(cls, a, b): return [
        c + d for c, d in cls.iterator(a, b)
    ]

    @classmethod
    def sub(cls, a, b): return [
        c - d for c, d in cls.iterator(a, b)
    ]

    @classmethod
    def mul(cls, a, b): return [
        c * d for c, d in cls.iterator(a, b)
    ]

    @classmethod
    def dot(cls, a, b): return sum(
        c * d for c, d in cls.iterator(a, b)
    )

    @classmethod
    def eq(cls, a, b): return (len(a) == len(b)) and all(
        c == d for c, d in cls.iterator(a, b)
    )

    @classmethod
    def ne(cls, a, b): return (len(a) != len(b)) or all(
        c != d for c, d in cls.iterator(a, b)
    )

    @classmethod
    def iterator(cls, a, b):
        if isinstance(a, Number):
            for i, _ in enumerate(b): yield a, b[i]
        elif isinstance(b, Number):
            for i, _ in enumerate(a): yield a[i], b
        else:
            for i, _ in enumerate(a): yield a[i], b[i]
