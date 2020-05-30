from pathlib import Path


def file_exists(path):
    return Path(path).exists()
