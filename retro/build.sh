#!/bin/bash

set -o errexit -o nounset

python -m retro.tests.font
python -m retro.tests.image
python -m retro.tests.sprite
