from pathlib import Path

import rootpath

ROOT_PATH = Path(rootpath.detect(__file__))


def to_path(result_path: str) -> Path:
    """Converts result path to Path object.
    result_path could be
    dir/file name
    Also it clouf be
    - absolute path
    - file/dir inside results dir"""
    path = Path(result_path)
    if path.exists():
        return path

    path = ROOT_PATH / "results" / result_path
    return path
