#!/bin/bash

set -o errexit -o nounset

retro/test.sh
python -m retro.tests.events
python -m retro.tests.scheduler --interactive
python -m retro.tests.image --interactive
python -m retro.tests.sprite --interactive

python -m pong.main
python -m maze.main
python -m shooter.main
python -m lemmings.main

python -m flappy.play_manual
python -m flappy.play_auto
python -m flappy.play_nnga

python -m pacman.play_manual
python -m pacman.play_auto
python -m pacman.play_nnga
