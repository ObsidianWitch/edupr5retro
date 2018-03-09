#!/bin/sh

mkdir -p 'out'
cat 'src/constants.py' \
    'src/surface.py' \
    'src/window.py' \
    'src/event.py' \
    > 'out/retro.py'
