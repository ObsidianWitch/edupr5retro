from src.constants import *
from src.window import Window

window = Window(
    title     = "window",
    size      = (640, 480),
    framerate = 30,
)

def main():
    window.fill(WHITE) \
        .draw_line(
            color     = GREEN,
            start_pos = (0, 0),
            end_pos   = (50,30),
            width     = 5,
        ).draw_rect(
            color = BLACK,
            rect  = (75, 10, 50, 20),
            width = 2,
        ).draw_rect(
            color = BLACK,
            rect  = (150, 10, 50, 20),
        ).draw_circle(
            color  = BLUE,
            center = (60, 250),
            radius  = 40,
        ).draw_circle(
            color  = BLUE,
            center = (200, 250),
            radius  = 40,
            width   = 4,
        )

window.loop(main)
