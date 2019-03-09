#!/bin/sh

dnewlines() { cat -s ; }
dimports() { sed -e '/^import/d' -e '/^from .* import/d' ; }
dcomments() { sed '/^\s*#/d' ; }
decorate() { cat ; echo ; }

mkdir -p 'out'

out1='out/retro.doc.py'
cat 'pr5retro/constants.py' | dnewlines | decorate > "$out1"
for f in 'pr5retro/rect.py' \
         'pr5retro/image.py' \
         'pr5retro/font.py' \
         'pr5retro/window.py' \
         'pr5retro/events.py' \
         'pr5retro/sprite.py' \
         'pr5retro/vector.py'
do cat "$f" | dimports | dnewlines | decorate >> "$out1"; done

out2='out/retro.py'
cat "$out1" | dcomments | dnewlines > "$out2"
