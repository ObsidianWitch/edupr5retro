from retro.src import retro

window = retro.Window(
    title = "window",
    size  = (640, 480),
    fps   = 30,
)

def main():
    # key - event
    e = window.events.event(retro.KEYDOWN)
    if e: print(e)
    e = window.events.event(retro.KEYUP)
    if e: print(e)

    # key - methods
    e = window.events.key_press(retro.K_F1)
    if e: print("press F1")
    e = window.events.key_hold(retro.K_F1)
    if e: print("hold F1")
    e = window.events.key_release(retro.K_F1)
    if e: print("release F1")

    # mouse- event
    e = window.events.event(retro.MOUSEBUTTONDOWN)
    if e: print(e)
    e = window.events.event(retro.MOUSEBUTTONUP)
    if e: print(e)

    # mouse- methods
    e = window.events.mouse_press(retro.M_LEFT)
    if e: print("press M_LEFT")
    e = window.events.mouse_hold(retro.M_LEFT)
    if e: print("hold M_LEFT")
    e = window.events.mouse_release(retro.M_LEFT)
    if e: print("release M_LEFT")
    # print(window.events.mouse_pos())

while 1:
    window.update(main)
