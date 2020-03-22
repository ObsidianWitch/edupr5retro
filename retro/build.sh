#!/bin/bash

set -o errexit -o nounset

python -m retro.tests.font
python -m retro.tests.image
python -m retro.tests.sprite

mypy --namespace-packages --ignore-missing-imports \
     --disallow-untyped-calls --disallow-untyped-defs \
     -m retro.src.retro
