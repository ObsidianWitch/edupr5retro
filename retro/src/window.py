import sys
import math
import typing as T
import pygame
from retro.src.image import Image
from retro.src.events import Events
from retro.src.font import Font

class Window(Image):
    def __init__(self, title, size, ups, fps, headless = False):
        pygame.init()

        self.headless = headless
        if self.headless:
            surface = pygame.Surface(size)
        else:
            pygame.display.set_caption(title)
            surface = pygame.display.set_mode(size)
        Image.__init__(self, surface)

        self.clock = pygame.time.Clock()
        self.ups = ups
        self.fps = fps
        self.tick = 0
        self.schedule = self.scheduler(self.ups, self.fps)

        self.events = Events()

        self.fonts = list( Font(size) for size in range(18, 43, 6) )

    def cursor(self, cursor: T.Union[bool, tuple]) -> None:
        if type(cursor) is bool:
            pygame.mouse.set_visible(cursor)
        else:
            pygame.mouse.set_visible(True)
            pygame.mouse.set_cursor(*cursor)

    # The scheduler allows to set different update and render frequencies. The
    # task with the highest frequency will always be allocated. The task with
    # the lowest frequency will be distributed as evenly as possible.
    #
    # Note: if ups or fps <= 0, the tasks won't be scheduled and they will run
    # as fast as possible (no limit).
    #
    # Example: ups=20 fps=17
    # UUUUUUUUUUUUUUUUUUUU
    # ____________________ init      -> slots=20 remaining=17
    # R_R_R_R_R_R_R_R_R_R_ divisor=2 -> slots=10 remaining=7
    # 'R'_'R'_'R'_'R'_'R'_ divisor=2 -> slots=5  remaining=2
    # '''R'''_'''_'''R'''_ divisor=3 -> slots=3  remaining=0
    @classmethod
    def scheduler(cls, ups, fps):
        if (ups <= 0 or fps <= 0) or (ups == fps):
            return lambda tick: (ups, True, True)

        slots, remaining = (ups, fps) if ups >= fps else (fps, ups)
        schedule = [ False for _ in range(slots) ]

        while remaining > 0:
            divisor = math.ceil(slots / remaining)
            for availi, schi in enumerate(
                schi for schi, val in enumerate(schedule) if not val
            ):
                if (not schedule[schi]) and (availi % divisor == 0):
                    schedule[schi] = True
                    slots -= 1
                    remaining -= 1

        if ups > fps:
            return lambda tick: (ups, True, schedule[tick % ups])
        else:
            return lambda tick: (fps, schedule[tick % fps], True)

    # Execute update and/or render each step of the application loop depending
    # on their schedule. They can be disabled by setting them to None.
    def step(self, update, render):
        self.events.update()
        if self.events.event(pygame.QUIT):
            sys.exit()

        limitrate, isUpdating, isRendering = self.schedule(self.tick)
        if update and isUpdating:
            update()
        if render and isRendering:
            render()
            pygame.display.flip()

        self.clock.tick(limitrate)
        self.tick += 1

    def loop(self, update, render):
        while True:
            self.step(update, render)
