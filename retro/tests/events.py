from retro.src.constants import *
from retro.src.window import Window

window = Window(
    title     = "window",
    size      = (640, 480),
    framerate = 30,
)

def main():
    # key - event
    e = window.events.event(KEYDOWN)
    if e: print(e)
    e = window.events.event(KEYUP)
    if e: print(e)

    # key - methods
    e = window.events.key_press(K_F1)
    if e: print("press F1")
    e = window.events.key_hold(K_F1)
    if e: print("hold F1")
    e = window.events.key_release(K_F1)
    if e: print("release F1")

    # mouse- event
    e = window.events.event(MOUSEBUTTONDOWN)
    if e: print(e)
    e = window.events.event(MOUSEBUTTONUP)
    if e: print(e)

    # mouse- methods
    e = window.events.mouse_press(M_LEFT)
    if e: print("press M_LEFT")
    e = window.events.mouse_hold(M_LEFT)
    if e: print("hold M_LEFT")
    e = window.events.mouse_release(M_LEFT)
    if e: print("release M_LEFT")
    # print(window.events.mouse_pos())

window.loop(main)
