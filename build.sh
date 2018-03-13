#!/bin/sh

build() {
    decorate() {
        cat
        echo
    }

    discard_newlines() {
        cat -s
    }

    discard_imports() {
        sed -e '/^import/d' \
            -e '/^from .* import/d'
    }

    discard_comments() {
        sed '/^\s*#/d'
    }

    out1='out/retro.full.py'
    mkdir -p `dirname "$out1"`
    echo -n > "$out1"
    cat 'src/constants.py' | discard_newlines | decorate >> "$out1"
    for f in 'src/rect.py' \
             'src/image.py' \
             'src/font.py' \
             'src/window.py' \
             'src/events.py'
    do cat "$f" | discard_imports | discard_newlines | decorate >> "$out1"; done

    out2='out/retro.py'
    echo -n > "$out2"
    cat "$out1" | discard_comments | discard_newlines >> "$out2"
}

doc() {
    out='doc/3_classes.md'
    ./doc.py > "$out"
}

build
doc
