from pathlib import Path


def file_exits(path):
    return Path(path).exists()
