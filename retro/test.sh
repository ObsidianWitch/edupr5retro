#!/bin/bash

set -o errexit -o nounset

python -m retro.tests.scheduler
python -m retro.tests.image
python -m retro.tests.sprite
