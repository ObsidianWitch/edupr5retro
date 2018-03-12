import collections
import include.retro as retro

MAZE_PALETTE = collections.defaultdict(
    lambda: retro.BLACK, {'B': retro.BLUE }
)

SPRITE_PALETTE = {
    ' ': retro.BLACK,
    'W': retro.WHITE,
    'R': retro.RED,
    'G': retro.GREEN,
    'B': retro.BLUE,
    'C': retro.CYAN,
    'Y': retro.YELLOW,
}
