import collections

class Directions:
    def __init__(self, up, down, left, right):
        self.up    = up
        self.down  = down
        self.left  = left
        self.right = right

    @property
    def vec(self): return [
        self.right - self.left,
        self.down  - self.up,
    ]

def clamp(val, minval, maxval): return max(minval, min(val, maxval))
