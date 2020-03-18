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

    def invert(self):
        helper = lambda v: not v if (v is not None) else None
        self.up    = helper(self.up)
        self.down  = helper(self.down)
        self.left  = helper(self.left)
        self.right = helper(self.right)
        return self

    def replace(self, old_v, new_v):
        helper = lambda v: new_v if (v == old_v) else v
        self.up    = helper(self.up)
        self.down  = helper(self.down)
        self.left  = helper(self.left)
        self.right = helper(self.right)
        return self

    def __contains__(self, v): return v in (
        self.up, self.down, self.left, self.right
    )

    def __repr__(self): return (
            "<Directions(\n"
            f"\tup: {self.up}\n"
            f"\tdown: {self.down}\n"
            f"\tleft: {self.left}\n"
            f"\tright: {self.right}\n"
            ")"
        )
