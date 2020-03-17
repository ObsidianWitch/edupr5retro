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
cd retro

./build.sh
python -m tests.{test} # e.g. python -m tests.sprite
~~~

## Flappy NNGA

~~~sh
cd flappy

python play_manual.py # play with space bar
python play_auto.py   # play automatically (simple condition)
python play_nnga.py   # play automatically (ANN with GA)
~~~

## Pacman NNGA

~~~sh
cd pacman

# play with arrow keys
python play_manual.py [--small]

# play automatically (heuristic)
python play_auto.py [--small]

# play automatically (ANN with GA)
python play_nnga.py [--small] [--parallel]

# Options
# --small: small maze
# --parallel: split computations between CPU cores
~~~
