import pygame

from lemmings.states.level import Level

class Level1(Level):
    def __init__(self, window):
        Level.__init__(
            self     = self,
            window   = window,
            map      = "map1.png",
            startp   = (250, 100),
            endp     = (622, 252),
        )
