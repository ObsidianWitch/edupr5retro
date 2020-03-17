from pathlib import Path

def asset(filename):
    return str(Path('lemmings/data') / filename)
