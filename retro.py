import time

class Clock:
    def __init__(self, framerate):
        self.period = (1 / framerate)
        self.timestart = time.time()

    def tick(self):
        delta = time.time() - self.timestart
        if (delta < self.period): time.sleep(self.period - delta)

        now = time.time()
        timepassed = now - self.timestart
        self.timestart = now

        return timepassed
