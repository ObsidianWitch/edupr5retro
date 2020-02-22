from pathlib import Path

def asset(filename):
    return str(Path('shooter/data') / filename)
