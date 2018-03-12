#!/bin/sh

build() {
    decorate() {
        echo "### begin $1" >> 'out/retro.py'
        $2 "$1" >> 'out/retro.py'
        echo "### end $1" >> 'out/retro.py'
    }

    discard_imports() {
        sed -e '/^import/d' \
            -e '/^from .* import/d'
    }

    discard_comments() {
        sed -e '/^\s*#/d'
    }

    discard_all() {
        cat "$1" | discard_imports | discard_comments
    }

    mkdir -p 'out'
    echo -n > 'out/retro.py'
    decorate 'src/constants.py' 'cat'
    for f in 'src/rect.py' \
             'src/image.py' \
             'src/font.py' \
             'src/window.py' \
             'src/event.py'
    do decorate "$f" 'discard_all'; done
}

build
