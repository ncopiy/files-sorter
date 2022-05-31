import os

from datetime import datetime, timezone
from pathlib import Path
from shutil import copy as shutil_copy
from typing import List


def get_target_path(destination, entry) -> str:
    stat = entry.stat()
    ts = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)

    return os.path.join(destination, ts.strftime("%Y"), ts.strftime("%m"), ts.strftime("%d"))


def main(paths: List[str], destination: str) -> None:
    path_to_existed = {}

    for i, path in enumerate(paths):
        for entry in os.scandir(path):
            if entry.is_dir():
                paths.append(entry.path)
                continue
            
            target = get_target_path(destination, entry)

            if target not in path_to_existed:
                path_to_existed[target] = True
                Path(target).mkdir(parents=True, exist_ok=True)

            target_with_name = os.path.join(target, entry.name)
            source = os.path.join(path, entry.name)

            shutil_copy(source, target_with_name)


if __name__ == '__main__':
    main(paths=[], destination="")
