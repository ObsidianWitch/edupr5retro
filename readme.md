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

Retro ([doc](https://obsidienne.gitlab.io/prretrolib)) is a python module
extending [pygame](https://www.pygame.org).

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
# play with arrow keys
python -m pacman.play_manual [--small]

# play automatically (heuristic)
python -m pacman.play_auto [--small]

# play automatically (ANN with GA)
python -m pacman.play_nnga [--small] [--parallel]

# Options
# --small: small maze
# --parallel: split computations between CPU cores
~~~
