#!/bin/sh

decorate() {
    echo "### begin $1" >> 'out/retro.py'
    $2 "$1" >> 'out/retro.py'
    echo "### end $1" >> 'out/retro.py'
}

# Discard imports and comments.
discard_elems() {
    sed -e '/^import/d' \
        -e '/^from .* import/d' \
        -e '/^\s*#/d' \
        "$1"
}

mkdir -p 'out'
echo -n > 'out/retro.py'
decorate 'src/constants.py' 'cat'
for f in 'src/rect.py' \
         'src/image.py' \
         'src/font.py' \
         'src/window.py' \
         'src/event.py'
do decorate "$f" 'discard_elems'; done
