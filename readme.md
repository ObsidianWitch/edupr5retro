# PR5 Retrogaming

## Atelier

~~~sh
python -m pong.main
python -m aquarium.main
python -m maze.main
python -m shooter.main
python -m lemmings.main
~~~

## Retro Module

Retro is a module containing tools shared between this repository's games.

### Dependencies

* (lib) [pygame](https://www.pygame.org)
* (lib) [numpy](http://www.numpy.org/)

### Build & tests

~~~sh
retro/build.sh
~~~

## Flappy NNGA

~~~sh
cd flappy

python -m flappy.play_manual # play with space bar
python -m flappy.play_auto   # play automatically (simple condition)
python -m flappy.play_nnga   # play automatically (ANN with GA)
~~~

## Pacman NNGA

~~~sh

python -m pacman.play_manual # play with arrow keys
python -m pacman.play_auto # play automatically (heuristic)
python -m pacman.play_nnga [--parallel] # play automatically (ANN with GA)
~~~
