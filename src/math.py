class Math:
    # Méthodes de classe

    ## ~~~{.python .prototype}
    ## clamp(val: Number, minval: Number, maxval: Number) -> Number
    ## ~~~
    ## Restreint `val` dans [`minval`, `maxval`].
    @classmethod
    def clamp(cls, val, minval, maxval):
        return minval if val < minval \
          else maxval if val > maxval \
          else val
