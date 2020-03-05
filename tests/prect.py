import cProfile
import pstats
from pygame import Rect as PygRect
from src.rect import Rect as RetroRect

# median 10 execs cumulative: 0.262 seconds
def profile_pyg_init():
    for i in range(0, 1000000):
        r0 = PygRect(i, i + 1, i + 2, i + 3)

# median 10 execs cumulative: 0.748 seconds
def profile_retro_init():
    for i in range(0, 1000000):
        r0 = RetroRect(i, i + 1, i + 2, i + 3)

# ---

# median 10 execs cumulative: 0.050 seconds
def profile_pyg_get():
    r0 = PygRect(10, 11, 12, 13)
    for _ in range(0, 1000000):
        r0.right

# median 10 execs cumulative: 0.834 seconds
def profile_retro_get():
    r0 = RetroRect(10, 11, 12, 13)
    for _ in range(0, 1000000):
        r0.right

# ---

# median 10 execs cumulative: 0.056 seconds
def profile_pyg_set():
    r0 = PygRect(10, 11, 12, 13)
    for i in range(0, 1000000):
        r0.right = i

# median 10 execs cumulative: 0.888 seconds
def profile_retro_set():
    r0 = RetroRect(10, 11, 12, 13)
    for i in range(0, 1000000):
        r0.right = i

# ---

# median 10 execs cumulative: 0.236 seconds
def profile_pyg_copy():
    r0 = PygRect(10, 11, 12, 13)
    for _ in range(0, 1000000):
        rc = r0.copy()

# median 10 execs cumulative: 1.083 seconds
def profile_retro_copy():
    r0 = RetroRect(10, 11, 12, 13)
    for _ in range(0, 1000000):
        rc = r0.copy()

# ---

with cProfile.Profile() as pr:
    profile_pyg_init()
    profile_retro_init()

    profile_pyg_get()
    profile_retro_get()

    profile_pyg_set()
    profile_retro_set()

    profile_pyg_copy()
    profile_retro_copy()
pstats.Stats(pr) \
    .sort_stats('cumulative') \
    .print_stats()
