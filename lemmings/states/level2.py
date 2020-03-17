from lemmings.states.level import Level

class Level2(Level):
    def __init__(self, window):
        Level.__init__(
            self     = self,
            window   = window,
            map      = "map2.png",
            startp   = (72, 14),
            endp     = (669, 66),
        )
