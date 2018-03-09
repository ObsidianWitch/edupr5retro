#!/bin/sh

mkdir -p 'out'
echo -n > 'out/retro.py'
for f in 'src/constants.py' \
         'src/surface.py' \
         'src/window.py' \
         'src/event.py'
do
    echo "### begin $f" >> 'out/retro.py'
    cat "$f" >> 'out/retro.py'
    echo "### end $f" >> 'out/retro.py'
done
