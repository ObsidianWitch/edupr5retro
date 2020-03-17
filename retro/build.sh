#!/bin/bash

set -o errexit -o nounset

mypy.main() {
    env mypy --namespace-packages --ignore-missing-imports \
        --disallow-untyped-calls "$@"
}

mypy.strict() {
    mypy.main --disallow-untyped-defs "$@"
}

dimports() { sed -e '/^import/d' -e '/^from .* import/d' ; }

mkdir -p 'out'
out='out/retro.py'
cat 'src/constants.py' > "$out"
for f in 'src/math.py' \
         'src/image.py' \
         'src/font.py' \
         'src/window.py' \
         'src/events.py' \
         'src/sprite.py' \
         'src/stage.py'
do
    mypy.main --module="$(sed -e "s:/:\.:" -e "s/\.py//" <<< "$f")"
    cat "$f" | dimports >> "$out"
done
cat -s "$out" | sponge "$out"
mypy.main "$out"
