import sys
import typing as T
import pygame
from retro.src.image import Image
from retro.src.events import Events
from retro.src.font import Font

class Window(Image):
    def __init__(self,
        title: str, size: T.Tuple[int, int], fps: int, headless: bool = False,
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
        self.fps = fps

        self.events = Events()

        self.fonts = list(
            Font(size) for size in range(18, 43, 6)
        )

    def cursor(self, cursor: T.Union[bool, tuple]) -> None:
        if type(cursor) is bool:
            pygame.mouse.set_visible(cursor)
        else:
            pygame.mouse.set_visible(True)
            pygame.mouse.set_cursor(*cursor)

    def update(self, instructions: T.Callable) -> None:
        self.events.update()
        if self.events.event(pygame.QUIT):
            sys.exit()

        instructions()

        if not self.headless:
            pygame.display.flip()
        self.clock.tick(self.fps)
