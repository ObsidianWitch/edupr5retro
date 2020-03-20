#!/bin/bash

set -o errexit -o nounset

python -m tests.font
python -m tests.image

mkdir -p 'out'
out='out/retro.py'
cat 'src/constants.py' > "$out"
for f in 'math.py' 'image.py' 'font.py' 'window.py' 'events.py' 'sprite.py' \
         'stage.py' 'directions.py' 'collisions.py'
do
    module="$(sed -e "s/\.py//" <<< "$f")"
    mypy --namespace-packages --ignore-missing-imports \
         --disallow-untyped-calls --module="src.$module"
    sed -e '/^import/d' -e '/^from .* import/d' "src/$f" >> "$out"
done
cat -s "$out" | sponge "$out"
