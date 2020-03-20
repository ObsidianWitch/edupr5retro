from pathlib import Path

def asset(filename):
    return str(Path('maze/assets') / filename)
