import typing as typ
from src.image import Image
from src.sprite import Sprite
from pygame import Rect

class Stage(Sprite):
    # A Stage is a Sprite which can be modified and then restored to its
    # original state (`self.original`). A specific portion of the sprite image
    # can be focused by manipulated `self.camera`.
    def __init__(self, path: str):
        self.original = Image.from_path(path)
        Sprite.__init__(self, [self.original.copy()])

    @property
    def camera(self) -> Rect:
        return self.rect
    @camera.setter
    def camera(self, rect: Rect) -> None:
        self.rect = rect

    ## Transform point `p` from camera space to stage space.
    def camera2stage(self, p: typ.Tuple[int, int]) -> typ.Tuple[int, int]:
        return (p[0] + self.camera.x, p[1] + self.camera.y)

    ## Transform point `p` from stage space to camera space.
    def stage2camera(self, p: typ.Tuple[int, int]) -> typ.Tuple[int, int]:
        return (p[0] - self.rect.x, p[1] - self.rect.y)

    ## Restore stage to its `self.original` state.
    def clear_all(self) -> None:
        self.image.draw_img(self.original, (0, 0))

    ## Restore a portion (`self.camera`) of the stage to its `self.original`
    ## state.
    def clear_focus(self) -> None:
        self.image.draw_img(self.original, self.camera.topleft, self.camera)
