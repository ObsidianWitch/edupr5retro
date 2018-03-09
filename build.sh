#!/bin/sh

discard_imports() {
    sed -e '/^import/d' -e '/^from .* import/d' "$1"
}

mkdir -p 'out'
echo -n > 'out/retro.py'
for f in 'src/constants.py' \
         'src/surface.py' \
         'src/window.py' \
         'src/event.py'
do
    echo "### begin $f" >> 'out/retro.py'
    if [ "$f" = 'src/constants.py' ]; then
        cat "$f" >> 'out/retro.py'
    else
        discard_imports "$f" >> 'out/retro.py'
    fi
    echo "### end $f" >> 'out/retro.py'
done
