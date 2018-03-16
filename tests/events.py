import sys
from src.constants import *
from src.window import Window
from src.events import Events

window = Window(
    title     = "window",
    size      = (640, 480),
    framerate = 30,
)
events = Events()

while 1:
    events.update()
    if events.event(QUIT): sys.exit()

    # key - event
    e = events.event(KEYDOWN)
    if e: print(e)
    e = events.event(KEYUP)
    if e: print(e)

    # key - methods
    e = events.key_press(K_F1)
    if e: print("press F1")
    e = events.key_hold(K_F1)
    if e: print("hold F1")
    e = events.key_release(K_F1)
    if e: print("release F1")

    # mouse- event
    e = events.event(MOUSEBUTTONDOWN)
    if e: print(e)
    e = events.event(MOUSEBUTTONUP)
    if e: print(e)

    # mouse- methods
    e = events.mouse_press(M_LEFT)
    if e: print("press M_LEFT")
    e = events.mouse_hold(M_LEFT)
    if e: print("hold M_LEFT")
    e = events.mouse_release(M_LEFT)
    if e: print("release M_LEFT")
    # print(events.mouse_pos())

    window.update()
