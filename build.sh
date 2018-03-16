#!/bin/sh

dnewlines() { cat -s ; }
dimports() { sed -e '/^import/d' -e '/^from .* import/d' ; }
dcomments() { sed '/^\s*#/d' ; }
decorate() { cat ; echo ; }
fdoc() {
    sed '/^\s*# /d' \
  | sed '/^\s*## ~~~/d' \
  | sed 's/##/#/' \
  | sed '/> \[/d'
}

mkdir -p 'out'

out1='out/retro.full.py'
cat 'src/constants.py' | dnewlines | decorate > "$out1"
for f in 'src/rect.py' \
         'src/image.py' \
         'src/font.py' \
         'src/window.py' \
         'src/events.py'
do cat "$f" | dimports | dnewlines | decorate >> "$out1"; done

out2='out/retro.doc.py'
cat "$out1" | fdoc | dnewlines > "$out2"

out3='out/retro.py'
cat "$out1" | dcomments | dnewlines > "$out3"
