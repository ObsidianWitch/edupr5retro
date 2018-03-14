#!/usr/bin/env python3

import subprocess
import re

# Input: Markdown
# Retrieve the documentation and organize it in 4 levels.
# #:    class
# ##:   section (inheritance, constructor, methods, class methods, properties)
# ###:  method prototype
# ####: description
def step1(lines):
    result = []
    for l in lines:
        cl = l.lstrip(" ") # current line

        if cl == "\n":
            result.append(cl)
        elif cl.startswith("class "):
            cl = re.sub("\(.*\)", "", cl)
            result.append(f"# Classe {cl[6:-2]}\n")
            result.append("\n")
        elif cl.startswith("#"):
            result.append(f"#{cl}")
    return result

# Input: Markdown
# Insert method blockquotes and remove header from descriptions.
def step2(lines):
    result = []
    method = False
    for i, l in enumerate(lines):
        cl = l            # current line
        pl = lines[i - 1] # previous line

        if cl.startswith("###"):
            if cl.startswith("### "): cl = cl[4:]
            else: cl = cl[3:]

            if cl.startswith("~~~{") and (".prototype" in cl):
                method = True
                result.append('<blockquote class="method">\n')

            result.append(cl)
        elif pl.startswith("###") and method:
            method = False
            result.append("</blockquote>\n")
            result.append(cl)
        else:
            result.append(cl)

    return result

# Input: HTML
# Mark interpuncts as comments for syntax highlighting in code blocks of class
# interpunct.
def step3(lines):
    result = []
    interpunct = False
    for i, l in enumerate(lines):
        cl = l # current line

        if ("<pre" in cl) and ('class="interpunct"' in cl): interpunct = True

        if interpunct:
            cl = re.sub("·", "<span class=co>·</span>", cl)

        if "</pre>" in cl: interpunct = False

        result.append(cl)

    return result

# Generate doc/3_classes.md
with open("out/retro.full.py") as f: lines = f.readlines()
result = "".join(step2(step1(lines)))
with open("doc/3_classes.md", "w") as f: f.write(result)

# Generate out/doc.html
subprocess.run(
    "pandoc "
    "doc/*.md "
    "--output=out/doc.html "
    "--standalone "
    "--toc "
    "--include-in-header=doc/style.css "
    "--template=doc/template ",
    shell = True,
)

# Modify and write out/doc.html
with open("out/doc.html") as f: lines = f.readlines()
result = "".join(step3(lines))
with open("out/doc.html", "w") as f: f.write(result)
