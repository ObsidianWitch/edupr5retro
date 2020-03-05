#!/bin/sh

set -o errexit -o nounset

mypy() {
    env mypy \
        --namespace-packages --ignore-missing-imports \
        --disallow-untyped-calls \
        "$@"
}

dnewlines() { cat -s ; }
dimports() { sed -e '/^import/d' -e '/^from .* import/d' ; }
dcomments() { sed '/^\s*#/d' ; }
decorate() { cat ; echo ; }

mkdir -p 'out'

out1='out/retro.doc.py'
cat 'src/constants.py' | dnewlines | decorate > "$out1"
for f in 'src/math.py' \
         'src/rect.py' \
         'src/image.py' \
         'src/font.py' \
         'src/window.py' \
         'src/events.py' \
         'src/sprite.py' \
         'src/stage.py'
do
    mypy --module="$(sed -e "s:/:\.:" -e "s/\.py//" <<< "$f")"
    cat "$f" | dimports | dnewlines | decorate >> "$out1"
done
mypy "$out1"


out2='out/retro.py'
cat "$out1" | dcomments | dnewlines > "$out2"
