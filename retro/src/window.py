import sys
import typing as typ
import pygame
from retro.src.image import Image
from retro.src.events import Events
from retro.src.font import Font

class Window(Image):
    def __init__(self,
        title: str, size: typ.Tuple[int, int], framerate: int = 30,
        headless: bool = False
    ) -> None:
        pygame.init()

        self.headless = headless
        if self.headless:
            surface = pygame.Surface(size)
        else:
            pygame.display.set_caption(title)
            surface = pygame.display.set_mode(size)
        Image.__init__(self, surface)

        self.clock = pygame.time.Clock()
        self.framerate = framerate

        self.events = Events()

        self.fonts = list(
            Font(size) for size in range(18, 43, 6)
        )

    # Return the number of milliseconds since the window has been initialized.
    @classmethod
    def time(cls) -> int:
        return pygame.time.get_ticks()

    def cursor(self, enable: bool) -> None:
        pygame.mouse.set_visible(enable)

    # Update the content of the window and limit the runtime speed of the game
    # to `self.framerate`.
    def update(self) -> None:
        self.dt = self.clock.tick(self.framerate)
        pygame.display.flip()

    # 1. retrieve new events
    # 2. execute `instructions`
    # 3. update the content of the window
    def loop(self, instructions: typ.Callable) -> None:
        while 1:
            self.events.update()
            if self.events.event(pygame.QUIT): sys.exit()

            instructions()

            self.update()
