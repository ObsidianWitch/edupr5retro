class Stage(Sprite):
    # Héritage

    ## > [Sprite](#classe-sprite)

    # Constructeur

    ## ~~~{.python .prototype}
    ## Stage(path:str) -> Stage
    ## ~~~
    ## Un Stage est un Sprite qui peut être altéré et restauré dans son état
    ## d'origine (`original:Image`). Il est possible de se focaliser sur une
    ## portion restreinte de l'image du sprite en manipulant `rect`/`camera`.
    def __init__(self, path):
        self.original = Image.from_path(path)
        Sprite.__init__(self, self.original.copy())

    # Propriétés

    ## ~~~{.python .prototype}
    ## camera -> Rect
    ## camera = rect:Rect
    ## ~~~
    @property
    def camera(self):
        return self.rect
    @camera.setter
    def camera(self, rect):
        self.rect = rect

    # Méthodes

    ## ~~~{.python .prototype}
    ## camera2stage(p: Tuple[int, int]) -> Tuple[int, int]
    ## ~~~
    ## Transform point `p` from camera space to stage space.
    def camera2stage(self, p): return (
        p[0] + self.camera.x,
        p[1] + self.camera.y,
    )

    ## ~~~{.python .prototype}
    ## stage2camera(p: Tuple[int, int]) -> Tuple[int, int]
    ## ~~~
    ## Transform point `p` from stage space to camera space.
    def stage2camera(self, p): return (
        p[0] - self.rect.x,
        p[1] - self.rect.y,
    )

    ## ~~~{.python .prototype}
    ## clear_all()
    ## ~~~
    ## Restore stage to its `self.original` state.
    def clear_all(self):
        self.image.draw_img(self.original, (0, 0))

    ## ~~~{.python .prototype}
    ## clear_focus()
    ## ~~~
    ## Restore a portion (`self.camera`) of the stage to its `self.original`
    ## state.
    def clear_focus(self):
        self.image.draw_img(self.original, self.camera.topleft, self.camera)
