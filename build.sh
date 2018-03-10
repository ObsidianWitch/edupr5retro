#!/bin/sh

decorate() {
    echo "### begin $1" >> 'out/retro.py'
    $2 "$1" >> 'out/retro.py'
    echo "### end $1" >> 'out/retro.py'
}

discard_imports() {
    sed -e '/^import/d' -e '/^from .* import/d' "$1"
}

mkdir -p 'out'
echo -n > 'out/retro.py'
decorate 'src/constants.py' 'cat'
for f in 'src/image.py' \
         'src/window.py' \
         'src/event.py'
do decorate "$f" 'discard_imports'; done
