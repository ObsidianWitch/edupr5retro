import pygame

class Timer:
    @property
    def time(self): return (pygame.time.get_ticks() // 1000)

    @property
    def elapsed(self): return (self.time - self.t0)

    @property
    def remaining(self): return (self.end - self.elapsed)

    @property
    def finished(self): return (self.elapsed >= self.end)

    def __init__(self, end):
        self.end = end
        self.restart()

    def restart(self): self.t0 = self.time
