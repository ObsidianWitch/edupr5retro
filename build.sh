#!/bin/sh

set -o errexit -o nounset

mypy() {
    env mypy \
        --namespace-packages --ignore-missing-imports \
        --disallow-untyped-calls \
        "$@"
}

dimports() { sed -e '/^import/d' -e '/^from .* import/d' ; }

mkdir -p 'out'
out='out/retro.py'
cat 'src/constants.py' > "$out"
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
    cat "$f" | dimports >> "$out"
done
cat -s "$out" | sponge "$out"
mypy "$out"
