from numbers import Real

class Math:
    @classmethod
    def distance(cls, p1, p2): return \
        abs(p2[0] - p1[0]) \
      + abs(p2[1] - p1[1])
