import types

class Parameters:
    @classmethod
    def classic(cls): return types.SimpleNamespace(
        name        = "classic",
        window_size = (448, 528),
        player_pos  = (208, 264),
        ghosts_pos  = (208, 168),
        ghosts_num  = 4,
    )

    @classmethod
    def small(cls): return types.SimpleNamespace(
        name        = "small",
        window_size = (320, 240),
        player_pos  = (8, 8),
        ghosts_pos  = (208, 168),
        ghosts_num  = 1,
    )
