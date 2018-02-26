import pygame

class Timer:
    def __init__(self, end = 0, period = 1000):
        self.end = end
        self.period = period
        self.restart()

    @property
    def time(self): return (pygame.time.get_ticks() // self.period)

    @property
    def elapsed(self): return (self.time - self.t0)

    @property
    def remaining(self): return (self.end - self.elapsed)

    @property
    def finished(self): return (self.elapsed >= self.end)

    def restart(self): self.t0 = self.time
