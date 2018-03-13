#!/usr/bin/env python3

# Retrieve the documentation and organize it in 4 levels.
# #:    class
# ##:   section (constructeur, méthodes, méthodes de classe, propriétés)
# ###:  method prototype
# ####: description
def step1(lines):
    result = []
    for l in lines:
        cl = l.lstrip(" ")

        if cl == "\n": result.append(cl)
        elif cl.startswith("class "): result.append(f"# Classe {cl[6:-2]}\n\n")
        elif cl.startswith("#"): result.append(f"#{cl}")
    return result

# Insert method prototypes inside markdown code blocks and remove header from
# descriptions.
def step2(lines):
    result = []
    for i, l in enumerate(lines):
        cl = l            # current line
        pl = lines[i - 1] # previous line

        if cl.startswith("### "):
            if not pl.startswith("### "): result.append("~~~python\n")
            result.append(cl[4:])
        else:
            if pl.startswith("### "): result.append("~~~\n")

            if cl == "####\n": result.append("\n")
            elif cl.startswith("#### "): result.append(cl[5:])
            else: result.append(cl)

    return result

with open("out/retro.full.py") as f: lines = f.readlines()
result = "".join(step2(step1(lines)))
with open("doc/3_classes.md", "w") as f: f.write(result)
