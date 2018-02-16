import enum

import pygame

from shared.window import Window
from pong.state_run import StateRun
from pong.state_end import StateEnd

window = Window(
    width  = 600,
    height = 400,
    title  = "Pong"
)

State = enum.Enum("State", "START RUN END")
state = State.START

state_run = None
state_end = None

def pong():
    global state
    global state_run
    global state_end

    if state == State.START:
        state_run = StateRun(window)
        state = State.RUN

    if state == State.RUN:
        winner = state_run.run()
        if winner != 0:
            del state_run
            state_end = StateEnd(window, winner)
            state = State.END

    elif state == State.END:
        restart = state_end.run()
        if restart:
            del state_end
            state_run = StateRun(window)
            state = State.RUN

window.loop(pong)
