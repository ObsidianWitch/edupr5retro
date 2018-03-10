import sys
from src.constants import *
from src.window import Window
from src.event import Event

window = Window(
    title     = "window",
    size      = (640, 480),
    framerate = 30,
)
events = Event()

while 1:
    events.update()
    if events.event(QUIT): sys.exit()

    def check(e):
        if e: print(e)

    # key - event
    check(events.event(KEYDOWN))
    check(events.event(KEYUP))

    # key - methods
    check(events.key_press(K_F1))
    check(events.key_held(K_F1))
    check(events.key_release(K_F1))

    # mouse- event
    check(events.event(MOUSEBUTTONDOWN))
    check(events.event(MOUSEBUTTONUP))

    # mouse- methods
    check(events.mouse_press(M_LEFT))
    check(events.mouse_held(M_LEFT))
    check(events.mouse_release(M_LEFT))
    # print(events.mouse_pos())

    window.update()
