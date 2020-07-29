import sys
from retro.src import retro
from pacman.game.game import Game

window = retro.Window(
    title = "Pacman",
    size  = (448, 528),
    fps   = 60,
)
game = Game()

def main():
    if not game.finished:
        maze = game.maze
        player = game.player
        ghosts = game.ghosts

        key = window.events.key_press
        if   key(retro.K_UP):    player.nxtdir = [ 0, -1]
        elif key(retro.K_DOWN):  player.nxtdir = [ 0,  1]
        elif key(retro.K_LEFT):  player.nxtdir = [-1,  0]
        elif key(retro.K_RIGHT): player.nxtdir = [ 1,  0]

        game.update()
        game.draw(window)
    else:
        game.reset()

window.loop(main)
