class Timer:
    # A timer counts from 0 to `end`. Its value is increased every `period` ms.
    def __init__(self, period=1000, end=0):
        self.end = end
        self.period = period
        self.restart()

    @property
    def elapsed(self):
        return (pygame.time.get_ticks() - self.start) // self.period

    @property
    def remaining(self):
        return (self.end - self.elapsed)

    @property
    def finished(self):
        return (self.elapsed >= self.end)

    def restart(self):
        self.start = pygame.time.get_ticks()

class Ticker(Timer):
    @classmethod
    def inject(cls, window):
        cls.window = window

    # A ticker counts from 0 to `end`. Its value is increased every `period`
    # game step/frame.
    def __init__(self, period=1, end=0):
        self.restart()
        self.end = end
        self.period = period

    @property
    def elapsed(self):
        return (self.window.ftick - self.start) // self.period

    def restart(self):
        self.start = self.window.ftick
