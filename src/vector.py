class Vector:
    @classmethod
    def add(cls, va, vb): return [
        va[i] + vb[i] for i, _ in enumerate(va)
    ]

    @classmethod
    def sub(cls, va, vb): return [
        va[i] - vb[i] for i, _ in enumerate(va)
    ]

    @classmethod
    def dot(cls, va, vb): return sum(
        va[i] * vb[i] for i, _ in enumerate(va)
    )

    @classmethod
    def eq(cls, va, vb): return (len(va) == len(vb)) and all(
        va[i] == vb[i] for i, _ in enumerate(va)
    )

    @classmethod
    def ne(cls, va, vb): return (len(va) != len(vb)) or all(
        va[i] != vb[i] for i, _ in enumerate(va)
    )
